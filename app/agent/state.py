from typing import TypedDict, List, Dict


class ScriptAgentState(TypedDict):

    # Input fields — populated from API request
    country: str
    topic_category: str
    niche_context: str
    prompt_strategy: str        # "few_shot" or "zero_shot"

    # Trend fields — populated by trend_discovery and trend_selection nodes
    trends: List[str]
    selected_trend: str

    # Research fields — populated by youtube_research and context_builder nodes
    youtube_videos: List[Dict]
    research_context: str

    # Generation fields — populated by prompt_builder and script_generation nodes
    prompt: str
    generated_script: Dict      # structured dict with keys: hook, intro, body, outro

    # Output fields — populated by confidence_score_node and response_formatter nodes
    confidence_score: float
    final_response: Dict        # final formatted API response written by response_formatter
