from langgraph.graph import StateGraph, END
from app.graph.state import TripState
from app.agents.research import research_node
from app.agents.weather import weather_node
from app.agents.hotel import hotel_node
from app.agents.budget import budget_node
from app.agents.logistics import logistics_node
from app.agents.activities import activities_node
from app.agents.planner import planner_node


def router_check(state: TripState) -> str:
    """
    Router decision function after Planner Agent.
    Determines if the plan needs hotel revision based on multiple quality signals.

    This implements the "Router Check" decision node from the architecture diagram.

    Returns:
    - "revise_hotel" if plan needs hotel improvement and we haven't hit max revisions
    - "activities" if plan is acceptable, continue to activities
    """
    plan = state.get('plan', '')
    hotel_recommendations = state.get('hotel_recommendations', '')
    revision_count = state.get('revision_count', 0)
    plan_quality_score = state.get('plan_quality_score', 0)

    # Maximum revisions to prevent infinite loops
    MAX_REVISIONS = 1  # Allow one retry (matching reference repo pattern)

    # If we've reached max revisions, continue regardless of quality
    if revision_count >= MAX_REVISIONS:
        return "activities"

    # Check if planner explicitly signals need for hotel revision
    # (Following reference repo pattern where planner returns "REVISE_HOTEL")
    if isinstance(plan, str) and "REVISE_HOTEL" in plan:
        return "revise_hotel"

    # Check for insufficient hotel data
    hotel_content_lower = hotel_recommendations.lower() if hotel_recommendations else ""
    hotel_missing_signals = [
        "unavailable" in hotel_content_lower,
        "no hotels" in hotel_content_lower,
        "not found" in hotel_content_lower,
        len(hotel_content_lower) < 100  # Too short to be useful
    ]

    if any(hotel_missing_signals):
        return "revise_hotel"

    # Check quality score if available
    # 8-10: Excellent, no revision needed
    # 6-7: Good, acceptable
    # 0-5: Needs improvement (revise hotel)
    if plan_quality_score > 0 and plan_quality_score < 6:
        return "revise_hotel"

    # Plan is acceptable, continue to activities
    return "activities"


def increment_revision(state: TripState) -> dict:
    """
    Node to increment revision counter before looping back to hotel.
    This tracks how many times we've tried to improve the hotel recommendations.
    """
    current_count = state.get('revision_count', 0)
    return {"revision_count": current_count + 1, "status": "revising_hotel"}


def finalize_itinerary(state: TripState) -> dict:
    """
    Final node to format and finalize the itinerary output.
    This is the last step before END.
    """
    plan = state.get('plan')
    if plan:
        return {"status": "completed", "plan": plan}
    else:
        return {"status": "failed"}


def build_graph():
    """
    Builds the LangGraph workflow matching the architecture diagram:

    Flow:
    START → Research → Weather → Hotel → Budget → Logistics → Planner
         → Router Check → [revise_hotel OR activities]
         → Activities → finalize_itinerary → END

    Revision Loop:
    If Router Check returns "revise_hotel":
        Planner → increment_revision → Hotel → Budget → Logistics → Planner
    """
    workflow = StateGraph(TripState)

    # Add all agent nodes
    workflow.add_node("research", research_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("hotel", hotel_node)
    workflow.add_node("budget", budget_node)
    workflow.add_node("logistics", logistics_node)
    workflow.add_node("activities", activities_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("increment_revision", increment_revision)
    workflow.add_node("finalize_itinerary", finalize_itinerary)

    # Define workflow edges matching the diagram

    # Entry point: Start with Research Agent
    workflow.set_entry_point("research")

    # Sequential flow through agents (as shown in diagram)
    workflow.add_edge("research", "weather")
    workflow.add_edge("weather", "hotel")
    workflow.add_edge("hotel", "budget")
    workflow.add_edge("budget", "logistics")
    workflow.add_edge("logistics", "planner")

    # Router Check: Conditional edge after Planner
    # Decision: Continue to Activities OR Revise Hotel
    workflow.add_conditional_edges(
        "planner",
        router_check,
        {
            "revise_hotel": "increment_revision",  # Loop back for hotel improvement
            "activities": "activities"  # Plan is good, continue to activities
        }
    )

    # Revision loop: increment → hotel → budget → logistics → planner
    workflow.add_edge("increment_revision", "hotel")

    # After Activities, finalize the itinerary
    workflow.add_edge("activities", "finalize_itinerary")

    # End after finalization
    workflow.add_edge("finalize_itinerary", END)

    return workflow.compile()
