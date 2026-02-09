from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import TripState
from app.core.prompts import HOTEL_SYSTEM_PROMPT
from app.tools.search_utils import run_searches, build_search_context
from app.tools.mocks import BookingMocks
from app.tools.hotel_search import search_hotels
from app.core.llm import get_llm
from datetime import datetime, timedelta

async def hotel_node(state: TripState):
    """
    Hotel Agent: Researches and recommends accommodations based on destination,
    budget, dates, and traveler preferences.

    Uses search_hotels tool to provide:
    - Real-time hotel search results from web
    - Direct booking platform links (Booking.com, Hotels.com, Airbnb, etc.)
    """
    spec = state['spec']
    research_notes = state.get('research_notes', '')
    weather_info = state.get('weather_info', '')
    revision_count = state.get('revision_count', 0)

    # Calculate check-in and check-out dates
    if spec.dates and isinstance(spec.dates, str):
        try:
            start_date = datetime.strptime(spec.dates.split(' to ')[0].strip(), '%Y-%m-%d')
            # Assuming dates format is "YYYY-MM-DD to YYYY-MM-DD"
            checkin = start_date.strftime('%Y-%m-%d')
            checkout = (start_date + timedelta(days=7)).strftime('%Y-%m-%d')  # Default 7 days
        except:
            checkin = datetime.now().strftime('%Y-%m-%d')
            checkout = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    else:
        checkin = datetime.now().strftime('%Y-%m-%d')
        checkout = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    llm = get_llm(temperature=0.3, max_tokens=8000)
    if not llm:
        # Use mock hotel data when no API key is available
        hotels = BookingMocks.search_hotels(spec.destination, spec.budget_tier)
        hotel_context = "\n\n=== ACCOMMODATION OPTIONS ===\n"
        for hotel in hotels:
            hotel_context += f"\n• {hotel.name} ({hotel.area})\n"
            hotel_context += f"  Price: ${hotel.price_per_night}/night\n"
            hotel_context += f"  Rating: {hotel.rating}/5.0\n"
            hotel_context += f"  Description: {hotel.description}\n"
            hotel_context += f"  Booking: {hotel.booking_link}\n"
        return {"hotel_recommendations": hotel_context}

    # Use search_hotels tool for structured hotel search with booking links
    hotel_search_results = search_hotels.invoke({
        "destination": spec.destination,
        "checkin_date": checkin,
        "checkout_date": checkout,
        "num_guests": spec.travelers,
        "budget_range": spec.budget_tier
    })

    # Build context from hotel search results
    hotel_context = "\n\n=== HOTEL SEARCH RESULTS ===\n"
    if hotel_search_results.get("hotels"):
        for hotel in hotel_search_results["hotels"]:
            hotel_context += f"\n• {hotel.get('name', 'Unknown Hotel')}\n"
            hotel_context += f"  {hotel.get('description', '')[:200]}\n"
            hotel_context += f"  Source: {hotel.get('booking_url', '')}\n"

    # Add booking platform links
    hotel_context += "\n\n=== DIRECT BOOKING PLATFORMS ===\n"
    if hotel_search_results.get("booking_platforms"):
        for platform, url in hotel_search_results["booking_platforms"].items():
            hotel_context += f"\n• {platform}: {url}\n"

    # Retry instruction if this is a revision
    retry_instruction = ""
    if revision_count > 0:
        retry_instruction = """
        IMPORTANT: Previous hotel search results were insufficient.
        Please BROADEN your recommendations. Consider:
        - Neighboring areas and districts
        - Alternative accommodation types (apartments, guesthouses)
        - Slightly outside budget range if needed
        - Any highly-rated options available
        """

    # Perform additional web searches for context
    search_queries = [
        f"best hotels in {spec.destination} {spec.budget_tier} budget 2026",
        f"{spec.destination} accommodation recommendations {spec.travel_style}",
        f"where to stay in {spec.destination} neighborhoods guide"
    ]

    search_results = run_searches(search_queries, max_results_per_query=4, max_total=12)
    search_context = build_search_context(search_results, max_items=12)

    prompt = ChatPromptTemplate.from_template(
        HOTEL_SYSTEM_PROMPT +
        "\n\n{retry_instruction}" +
        "\n\nHotel Search Tool Results:\n{hotel_context}" +
        "\n\nAdditional Web Search Context:\n{search_context}"
    )
    chain = prompt | llm

    response = await chain.ainvoke({
        "destination": spec.destination,
        "dates": f"{checkin} to {checkout}",
        "budget_tier": spec.budget_tier,
        "travelers": spec.travelers,
        "travel_style": spec.travel_style,
        "interests": ", ".join(spec.interests) if spec.interests else "general sightseeing",
        "research_notes": research_notes,
        "weather_info": weather_info,
        "retry_instruction": retry_instruction,
        "hotel_context": hotel_context,
        "search_context": search_context
    })

    return {"hotel_recommendations": response.content}
