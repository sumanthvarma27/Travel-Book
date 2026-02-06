from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph.state import TripState
from app.core.prompts import HOTEL_SYSTEM_PROMPT
from app.tools.mocks import BookingMocks
import os

async def hotel_node(state: TripState):
    """
    Hotel Agent: Researches and recommends accommodations based on destination,
    budget, dates, and traveler preferences.
    """
    spec = state['spec']
    research_notes = state.get('research_notes', '')
    weather_info = state.get('weather_info', '')

    # Check for API key to decide execution mode
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
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

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.3)

    prompt = ChatPromptTemplate.from_template(HOTEL_SYSTEM_PROMPT)
    chain = prompt | llm

    response = await chain.ainvoke({
        "destination": spec.destination,
        "dates": spec.dates,
        "budget_tier": spec.budget_tier,
        "travelers": spec.travelers,
        "travel_style": spec.travel_style,
        "interests": ", ".join(spec.interests) if spec.interests else "general sightseeing",
        "research_notes": research_notes,
        "weather_info": weather_info
    })

    return {"hotel_recommendations": response.content}
