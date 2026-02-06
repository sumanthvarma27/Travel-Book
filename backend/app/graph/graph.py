from langgraph.graph import StateGraph, END
from app.graph.state import TripState
from app.agents.research import research_node
from app.agents.weather import weather_node
from app.agents.hotel import hotel_node
from app.agents.budget import budget_node
from app.agents.logistics import logistics_node
from app.agents.activities import activities_node
from app.agents.planner import planner_node


def should_revise(state: TripState) -> str:
    """
    Decision function to determine if the plan needs revision.
    This is called after the planner node to evaluate plan quality.

    Returns:
    - "revise" if plan needs improvement and we haven't hit max revisions
    - "end" if plan is good enough or max revisions reached
    """
    plan_quality_score = state.get('plan_quality_score', 0)
    revision_count = state.get('revision_count', 0)
    plan = state.get('plan')

    # Maximum revisions to prevent infinite loops
    MAX_REVISIONS = 2

    # If we've reached max revisions, end regardless of quality
    if revision_count >= MAX_REVISIONS:
        return "end"

    # If no plan was generated, end (can't revise nothing)
    if plan is None:
        return "end"

    # Quality thresholds:
    # 8-10: Excellent, no revision needed
    # 6-7: Good, acceptable
    # 0-5: Needs improvement
    if plan_quality_score >= 7:
        return "end"

    # Plan needs revision
    return "revise"


def increment_revision(state: TripState) -> dict:
    """
    Node to increment revision counter before looping back.
    This tracks how many times we've tried to improve the plan.
    """
    current_count = state.get('revision_count', 0)
    return {"revision_count": current_count + 1}


def build_graph():
    workflow = StateGraph(TripState)

    # Add all agent nodes
    workflow.add_node("weather", weather_node)
    workflow.add_node("research", research_node)
    workflow.add_node("hotel", hotel_node)
    workflow.add_node("logistics", logistics_node)
    workflow.add_node("budget", budget_node)
    workflow.add_node("activities", activities_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("increment_revision", increment_revision)

    # Define workflow edges
    # Entry point: Start with weather
    workflow.set_entry_point("weather")

    # Sequential flow through agents
    # Weather -> Research -> Hotel -> Logistics -> Budget -> Activities -> Planner
    workflow.add_edge("weather", "research")
    workflow.add_edge("research", "hotel")
    workflow.add_edge("hotel", "logistics")
    workflow.add_edge("logistics", "budget")
    workflow.add_edge("budget", "activities")
    workflow.add_edge("activities", "planner")

    # CYCLIC WORKFLOW: Conditional edge after planner
    # Planner evaluates the plan quality and decides whether to revise
    workflow.add_conditional_edges(
        "planner",
        should_revise,
        {
            "revise": "increment_revision",  # Loop back for improvement
            "end": END  # Plan is good enough, finish
        }
    )

    # After incrementing revision, loop back to research
    # This allows agents to regenerate with updated context
    workflow.add_edge("increment_revision", "research")

    return workflow.compile()
