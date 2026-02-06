from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from app.graph.state import TripState
from app.core.prompts import HOTEL_SYSTEM_PROMPT
from app.tools.web_search import web_search_tool
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
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project:
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

    # Perform web searches for hotel recommendations
    search_queries = [
        f"best hotels in {spec.destination} {spec.budget_tier} budget 2026",
        f"{spec.destination} accommodation recommendations {spec.travel_style}",
        f"where to stay in {spec.destination} {spec.travelers} travelers"
    ]

    search_results = []
    for query in search_queries:
        try:
            results = web_search_tool.invoke({"query": query, "max_results": 4})
            search_results.extend(results)
        except Exception as e:
            print(f"Search error for '{query}': {e}")

    # Format search results for LLM
    search_context = "\n\n".join([
        f"**{r['title']}**\n{r['snippet']}\nSource: {r['url']}"
        for r in search_results[:12]
    ])

    llm = ChatVertexAI(
        model="gemini-2.5-flash",
        project=project,
        location=location,
        temperature=0.3,
        max_tokens=8000
    )

    prompt = ChatPromptTemplate.from_template(
        HOTEL_SYSTEM_PROMPT + "\n\nWeb Search Results:\n{search_context}"
    )
    chain = prompt | llm

    response = await chain.ainvoke({
        "destination": spec.destination,
        "dates": spec.dates,
        "budget_tier": spec.budget_tier,
        "travelers": spec.travelers,
        "travel_style": spec.travel_style,
        "interests": ", ".join(spec.interests) if spec.interests else "general sightseeing",
        "research_notes": research_notes,
        "weather_info": weather_info,
        "search_context": search_context
    })

    return {"hotel_recommendations": response.content}
