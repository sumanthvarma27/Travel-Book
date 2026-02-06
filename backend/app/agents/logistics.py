from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph.state import TripState
from app.core.prompts import LOGISTICS_SYSTEM_PROMPT
from app.tools.mocks import BookingMocks
import os

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

    # Check for API key to decide execution mode
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
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

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.3)

    prompt = ChatPromptTemplate.from_template(LOGISTICS_SYSTEM_PROMPT)
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
        "weather_info": weather_info
    })

    return {"logistics_info": response.content}
