from typing import List, Dict
from pathlib import Path
from datetime import datetime, timezone
from app.agent.state import ScriptAgentState
from app.services.trends import fetch_trends
from app.services.youtube import search_videos
from app.services.llm import generate_script


# Removed mock fallbacks per user request to ensure real execution


def input_validation(state: ScriptAgentState) -> ScriptAgentState:

    for field in ["country", "topic_category"]:
        if field not in state or not state[field]:
            raise ValueError(f"Missing required field: {field}")

    if not state.get("prompt_strategy"):
        state["prompt_strategy"] = "few_shot"

    return state


def trend_discovery(state: ScriptAgentState) -> ScriptAgentState:

    trends = fetch_trends(state["country"])
    if not trends:
        raise ValueError("Empty trends returned from Google Trends RSS")

    state["trends"] = trends

    return state


def trend_selection(state: ScriptAgentState) -> ScriptAgentState:

    trends = state["trends"]
    niche = state.get("niche_context", "").lower()

    selected = None
    if niche:
        for trend in trends:
            if any(word in trend.lower() for word in niche.split()):
                selected = trend
                break

    if not selected:
        selected = trends[0]

    state["selected_trend"] = selected

    return state


def youtube_research(state: ScriptAgentState) -> ScriptAgentState:

    trend = state["selected_trend"]

    videos = search_videos(trend)
    if not videos:
        raise ValueError("No videos returned from YouTube API")

    state["youtube_videos"] = videos

    return state


def context_builder(state: ScriptAgentState) -> ScriptAgentState:

    context_parts = []

    for i, v in enumerate(state["youtube_videos"], 1):
        context_parts.append(
            f"Video {i}:\n"
            f"  Title: {v.get('title', 'N/A')}\n"
            f"  Description: {v.get('description', 'N/A')}\n"
            f"  Channel: {v.get('channel', 'N/A')}"
        )

    state["research_context"] = "\n\n".join(context_parts)

    return state


def prompt_builder(state: ScriptAgentState) -> ScriptAgentState:

    trend = state["selected_trend"]
    context = state["research_context"]
    strategy = state.get("prompt_strategy", "few_shot")

    if strategy == "few_shot":

        try:
            examples = Path("app/prompts/fewshot_prompt.md").read_text()
        except FileNotFoundError:
            examples = ""
            print("[prompt_builder] fewshot_prompt.md not found, falling back to zero_shot")

        prompt = f"""{examples}

---

NOW GENERATE A NEW SCRIPT:

Trend: {trend}

YouTube Research Context:
{context}

Instructions:
Respond ONLY in this exact JSON format with no extra text outside the JSON:
{{
  "hook": "1-2 punchy sentences to grab attention immediately",
  "intro": "2-3 sentences introducing the topic",
  "body": "4-6 sentences covering key insights drawn from the YouTube research context above",
  "outro": "1-2 sentences with a clear call to action"
}}
"""

    else:
        prompt = f"""Generate a YouTube video script about: {trend}

Context from YouTube research:
{context}

Respond ONLY in this exact JSON format with no extra text outside the JSON:
{{
  "hook": "...",
  "intro": "...",
  "body": "...",
  "outro": "..."
}}
"""

    state["prompt"] = prompt

    return state


def script_generation(state: ScriptAgentState) -> ScriptAgentState:

    script_dict = generate_script(state["prompt"])

    state["generated_script"] = script_dict

    return state


def confidence_score_node(state: ScriptAgentState) -> ScriptAgentState:
    # Named confidence_score_node to avoid naming conflict with state field confidence_score

    score = 0.5

    if len(state.get("youtube_videos", [])) >= 3:
        score += 0.2

    high_interest_keywords = ["AI", "Apple", "OpenAI", "Bitcoin", "ChatGPT", "Google"]
    trend = state.get("selected_trend", "")
    if any(kw.lower() in trend.lower() for kw in high_interest_keywords):
        score += 0.2

    if state.get("prompt_strategy") == "few_shot":
        score += 0.1

    state["confidence_score"] = round(min(score, 1.0), 2)

    return state


def response_formatter(state: ScriptAgentState) -> ScriptAgentState:
    # Writes the final API response into state["final_response"] and returns full state.
    # Must not return a plain dict — that would break LangGraph state management.

    state["final_response"] = {
        "trend": state["selected_trend"],
        "confidence_score": state["confidence_score"],
        "youtube_references": state["youtube_videos"],
        "generated_script": state["generated_script"],
        "prompt_strategy": state.get("prompt_strategy", "few_shot"),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

    return state
