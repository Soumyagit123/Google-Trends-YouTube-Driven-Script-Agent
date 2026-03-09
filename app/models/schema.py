from pydantic import BaseModel, Field
from typing import List, Dict


class ScriptRequest(BaseModel):
    country: str = Field(..., example="IN", description="Country code: IN, US, UK, etc.")
    topic_category: str = Field(..., example="tech", description="Category: tech, finance, entertainment")
    niche_context: str = Field(default="", example="AI tools for developers")
    prompt_strategy: str = Field(default="few_shot", example="few_shot", description="few_shot or zero_shot")


class ScriptResponse(BaseModel):
    trend: str
    confidence_score: float
    youtube_references: List[Dict]
    generated_script: Dict          # keys: hook, intro, body, outro
    prompt_strategy: str
    generated_at: str               # ISO 8601 timestamp
