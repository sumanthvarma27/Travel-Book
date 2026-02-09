from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import TripState
from app.core.prompts import LOGISTICS_SYSTEM_PROMPT
from app.tools.search_utils import run_searches, build_search_context
from app.tools.mocks import BookingMocks
from app.core.llm import get_llm

async def logistics_node(state: TripState):
    """
    Logistics Agent: Plans transportation including flights, intercity travel,
    local transport options, and routing recommendations.
    """
    spec = state['spec']
    research_notes = state.get('research_notes', '')
    weather_info = state.get('weather_info', '')

    # Parse dates
    try:
        start, end = spec.dates.split(' to ')
        start_date = start.strip()
        end_date = end.strip()
    except:
        import datetime
        today = datetime.date.today()
        start_date = today.strftime("%Y-%m-%d")
        end_date = (today + datetime.timedelta(days=3)).strftime("%Y-%m-%d")

    llm = get_llm(temperature=0.3, max_tokens=8000)
    if not llm:
        # Use mock flight data
        flights = BookingMocks.search_flights(spec.origin, spec.destination, start_date)
        return_flights = BookingMocks.search_flights(spec.destination, spec.origin, end_date)

        logistics_context = "\n\n=== TRANSPORTATION PLAN ===\n"
        logistics_context += "\n🛫 OUTBOUND FLIGHTS:\n"
        for flight in flights:
            logistics_context += f"  • {flight.provider}: {flight.departure} → {flight.arrival}\n"
            logistics_context += f"    Price: ${flight.estimated_price}\n"
            logistics_context += f"    Booking: {flight.booking_link}\n"

        logistics_context += "\n🛬 RETURN FLIGHTS:\n"
        for flight in return_flights:
            logistics_context += f"  • {flight.provider}: {flight.departure} → {flight.arrival}\n"
            logistics_context += f"    Price: ${flight.estimated_price}\n"
            logistics_context += f"    Booking: {flight.booking_link}\n"

        logistics_context += "\n🚇 LOCAL TRANSPORT:\n"
        logistics_context += f"  • Public transit (subway/bus): Recommended for {spec.destination}\n"
        logistics_context += f"  • Ride-sharing apps (Uber/Lyft): Available\n"
        logistics_context += f"  • Bike rentals: Available in central areas\n"
        logistics_context += f"  • Walking: Best for exploring local neighborhoods\n"

        return {"logistics_info": logistics_context}

    # Perform web searches for transportation options
    search_queries = [
        f"flights from {spec.origin} to {spec.destination} {start_date} 2026",
        f"best way to get around {spec.destination} public transport",
        f"{spec.destination} airport to city center transportation",
        f"transportation tips {spec.destination} {spec.budget_tier} budget"
    ]

    search_results = run_searches(search_queries, max_results_per_query=4, max_total=12)
    search_context = build_search_context(search_results, max_items=12)

    prompt = ChatPromptTemplate.from_template(
        LOGISTICS_SYSTEM_PROMPT + "\n\nWeb Search Results:\n{search_context}"
    )
    chain = prompt | llm

    response = await chain.ainvoke({
        "origin": spec.origin,
        "destination": spec.destination,
        "dates": spec.dates,
        "start_date": start_date,
        "end_date": end_date,
        "travelers": spec.travelers,
        "budget_tier": spec.budget_tier,
        "travel_style": spec.travel_style,
        "research_notes": research_notes,
        "weather_info": weather_info,
        "search_context": search_context
    })

    return {"logistics_info": response.content}
