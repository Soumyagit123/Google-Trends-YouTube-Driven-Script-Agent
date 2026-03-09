from langgraph.graph import StateGraph, END
from app.agent.state import ScriptAgentState
from app.agent.nodes import (
    input_validation,
    trend_discovery,
    trend_selection,
    youtube_research,
    context_builder,
    prompt_builder,
    script_generation,
    confidence_score_node,
    response_formatter
)


def build_graph():

    builder = StateGraph(ScriptAgentState)

    builder.add_node("input_validation", input_validation)
    builder.add_node("trend_discovery", trend_discovery)
    builder.add_node("trend_selection", trend_selection)
    builder.add_node("youtube_research", youtube_research)
    builder.add_node("context_builder", context_builder)
    builder.add_node("prompt_builder", prompt_builder)
    builder.add_node("script_generation", script_generation)
    builder.add_node("confidence_score_node", confidence_score_node)
    builder.add_node("response_formatter", response_formatter)

    builder.set_entry_point("input_validation")

    builder.add_edge("input_validation", "trend_discovery")
    builder.add_edge("trend_discovery", "trend_selection")
    builder.add_edge("trend_selection", "youtube_research")
    builder.add_edge("youtube_research", "context_builder")
    builder.add_edge("context_builder", "prompt_builder")
    builder.add_edge("prompt_builder", "script_generation")
    builder.add_edge("script_generation", "confidence_score_node")
    builder.add_edge("confidence_score_node", "response_formatter")
    builder.add_edge("response_formatter", END)

    return builder.compile()


graph = build_graph()
