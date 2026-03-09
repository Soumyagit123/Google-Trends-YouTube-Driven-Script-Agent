import app.config  # Ensures dotenv loads before anything else
from fastapi import FastAPI, Query
from app.agent.graph import graph
from app.models.schema import ScriptRequest

app = FastAPI(
    title="AI Trend Script Agent",
    description="Agentic YouTube script generator: Google Trends + YouTube Research + Claude",
    version="1.0.0"
)

SAMPLE_RESPONSE = {
    "trend": "OpenAI Sora",
    "confidence_score": 0.9,
    "youtube_references": [
        {
            "title": "Sora AI Explained",
            "description": "OpenAI's video generation model — what it does and why it matters.",
            "channel": "AI Daily"
        },
        {
            "title": "Sora vs Runway vs Pika",
            "description": "Comparing the top AI video generation tools available right now.",
            "channel": "Creator Tools"
        },
        {
            "title": "How to Use OpenAI Sora",
            "description": "Step-by-step walkthrough of Sora's text-to-video capabilities.",
            "channel": "Tech Simplified"
        }
    ],
    "generated_script": {
        "hook": "AI just changed filmmaking forever — and most people completely missed it.",
        "intro": "OpenAI recently released Sora, a model that generates cinematic-quality video directly from text prompts. No cameras, no crews, no expensive equipment.",
        "body": "Creators can now produce realistic scenes, actors, and environments entirely from text descriptions. Independent filmmakers who once needed six-figure budgets can now produce broadcast-quality content on a laptop. Advertisers are already using Sora to generate campaign videos in hours instead of weeks. The creative barrier to entry has dropped dramatically — but this also raises questions about authenticity and copyright.",
        "outro": "Will AI replace traditional video production entirely, or will it become the ultimate creative tool? Drop your prediction in the comments and subscribe for weekly AI updates."
    },
    "prompt_strategy": "few_shot",
    "generated_at": "2026-03-06T10:00:00+00:00"
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-script")
def generate_script_endpoint(
    request: ScriptRequest,
    mock: bool = Query(default=False, description="Return sample response for demo purposes")
):
    if mock:
        return SAMPLE_RESPONSE

    result = graph.invoke({
        "country": request.country,
        "topic_category": request.topic_category,
        "niche_context": request.niche_context,
        "prompt_strategy": request.prompt_strategy
    })

    return result["final_response"]
