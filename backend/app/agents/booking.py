from app.graph.state import TripState
from app.tools.mocks import BookingMocks

async def booking_node(state: TripState):
    spec = state['spec']
    
    # In a full agentic flow, this would be an LLM deciding what to search.
    # For MVP, we run the mocks deterministically based on input.
    
    hotels = BookingMocks.search_hotels(spec.destination, spec.budget_tier)
    # We cheat slightly and stick these into the state for the planner to 'see' via context
    # ideally, we'd add strictly typed fields for these in State.
    
    # For now, we will format them as string context for the Planner
    booking_context = f"\nFound Hotels: {[h.name + ' (' + str(h.price_per_night) + ')' for h in hotels]}"
    
    # We can also start enforcing the structure by returning partials if we wanted.
    
    return {"research_notes": booking_context} # Appending to research notes for simplicity
