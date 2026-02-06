from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from app.graph.state import TripState
from app.core.prompts import ACTIVITIES_SYSTEM_PROMPT
from app.tools.web_search import web_search_tool
import os

async def activities_node(state: TripState):
    """
    Activities Agent: Finds and recommends bookable activities, tours, experiences,
    and dining options with direct booking links from platforms like Viator,
    GetYourGuide, TripAdvisor, and OpenTable.
    """
    spec = state['spec']
    research_notes = state.get('research_notes', '')
    weather_info = state.get('weather_info', '')
    hotel_recommendations = state.get('hotel_recommendations', '')

    # Calculate trip duration
    try:
        start, end = spec.dates.split(' to ')
        from datetime import datetime
        start_date = datetime.strptime(start.strip(), "%Y-%m-%d")
        end_date = datetime.strptime(end.strip(), "%Y-%m-%d")
        num_days = (end_date - start_date).days + 1
    except:
        num_days = 3  # Default fallback

    # Check for API key to decide execution mode
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project:
        # Provide mock activities with booking links
        activities_context = f"\n\n=== ACTIVITIES & EXPERIENCES ===\n"
        activities_context += f"Based on your interests: {', '.join(spec.interests) if spec.interests else 'general sightseeing'}\n\n"

        # Generate destination-specific search links
        dest_encoded = spec.destination.replace(' ', '+')

        activities_context += "🎯 TOURS & ACTIVITIES:\n"
        activities_context += f"  • Walking Tour of {spec.destination}\n"
        activities_context += f"    Platform: GetYourGuide\n"
        activities_context += f"    Link: https://www.getyourguide.com/s/?q={dest_encoded}+walking+tour\n\n"

        activities_context += f"  • Food & Culture Tour\n"
        activities_context += f"    Platform: Viator\n"
        activities_context += f"    Link: https://www.viator.com/searchResults/all?text={dest_encoded}+food+tour\n\n"

        activities_context += f"  • Skip-the-Line Museum Passes\n"
        activities_context += f"    Platform: GetYourGuide\n"
        activities_context += f"    Link: https://www.getyourguide.com/s/?q={dest_encoded}+museum\n\n"

        if spec.interests:
            for interest in spec.interests[:2]:
                interest_encoded = interest.replace(' ', '+')
                activities_context += f"  • {interest.title()} Experience\n"
                activities_context += f"    Platform: Viator\n"
                activities_context += f"    Link: https://www.viator.com/searchResults/all?text={dest_encoded}+{interest_encoded}\n\n"

        activities_context += "🍽️ DINING RESERVATIONS:\n"
        activities_context += f"  • Top-rated restaurants in {spec.destination}\n"
        activities_context += f"    Platform: OpenTable\n"
        activities_context += f"    Link: https://www.opentable.com/s?covers=2&dateTime={spec.dates.split(' to ')[0]}+19:00&metroId=&regionIds=&term={dest_encoded}\n\n"

        activities_context += f"  • Local food experiences\n"
        activities_context += f"    Platform: TripAdvisor\n"
        activities_context += f"    Link: https://www.tripadvisor.com/Restaurants-g{dest_encoded}\n\n"

        activities_context += "💡 SUGGESTED DAILY ACTIVITIES:\n"
        activities_context += f"  Day 1: Arrival, light exploration, welcome dinner\n"
        activities_context += f"  Day 2-{num_days-1}: Mix of tours, activities, and free time\n"
        activities_context += f"  Day {num_days}: Final exploration and departure\n"

        return {"activities_recommendations": activities_context}

    # Perform web searches for activities and experiences
    interests_str = ' '.join(spec.interests) if spec.interests else 'sightseeing'
    search_queries = [
        f"best tours and activities in {spec.destination} 2026",
        f"{spec.destination} {interests_str} experiences",
        f"things to do {spec.destination} {spec.budget_tier} budget",
        f"top rated restaurants {spec.destination}",
        f"{spec.destination} food tours and dining experiences"
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
        for r in search_results[:15]
    ])

    llm = ChatVertexAI(
        model="gemini-2.5-flash",
        project=project,
        location=location,
        temperature=0.4,
        max_tokens=8000
    )

    prompt = ChatPromptTemplate.from_template(
        ACTIVITIES_SYSTEM_PROMPT + "\n\nWeb Search Results:\n{search_context}"
    )
    chain = prompt | llm

    response = await chain.ainvoke({
        "destination": spec.destination,
        "dates": spec.dates,
        "num_days": num_days,
        "travelers": spec.travelers,
        "budget_tier": spec.budget_tier,
        "travel_style": spec.travel_style,
        "interests": ", ".join(spec.interests) if spec.interests else "general sightseeing",
        "research_notes": research_notes,
        "weather_info": weather_info,
        "hotel_recommendations": hotel_recommendations,
        "search_context": search_context
    })

    return {"activities_recommendations": response.content}
