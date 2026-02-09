from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import TripState
from app.core.prompts import ACTIVITIES_SYSTEM_PROMPT
from app.tools.search_utils import run_searches, build_search_context
from app.tools.activity_bookings import find_activity_bookings
from app.core.llm import get_llm
import re

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

    llm = get_llm(temperature=0.4, max_tokens=8000)
    if not llm:
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

    # Extract key activities from itinerary/research notes to find booking links
    # Parse potential activities from research notes and plan
    plan = state.get('plan', '')
    activities_to_search = []

    # Extract activities from interests
    if spec.interests:
        for interest in spec.interests[:3]:
            activities_to_search.append(f"{interest} experience in {spec.destination}")

    # Add common activities
    activities_to_search.extend([
        f"Walking tour {spec.destination}",
        f"Food tour {spec.destination}",
        f"Museum tickets {spec.destination}"
    ])

    # Use find_activity_bookings tool to get structured booking options
    activity_booking_results = find_activity_bookings.invoke({
        "destination": spec.destination,
        "activities": activities_to_search,
        "max_results": 3
    })

    # Build context from activity booking results
    activity_context = "\n\n=== ACTIVITY BOOKING OPTIONS ===\n"
    if activity_booking_results.get("activities"):
        for activity_data in activity_booking_results["activities"]:
            activity_context += f"\n🎯 {activity_data.get('activity', 'Unknown Activity')}\n"
            for option in activity_data.get("booking_options", [])[:3]:
                activity_context += f"  • {option.get('title', 'Tour')}\n"
                activity_context += f"    Platform: {option.get('platform', 'Other')}\n"
                activity_context += f"    Link: {option.get('url', '')}\n"
                activity_context += f"    {option.get('snippet', '')[:150]}\n"

    # Add platform landing pages
    activity_context += "\n\n=== BOOKING PLATFORM LINKS ===\n"
    if activity_booking_results.get("platform_links"):
        for platform, url in activity_booking_results["platform_links"].items():
            activity_context += f"• {platform}: {url}\n"

    # Perform additional web searches for activities and experiences
    interests_str = ' '.join(spec.interests) if spec.interests else 'sightseeing'
    search_queries = [
        f"best tours and activities in {spec.destination} 2026",
        f"{spec.destination} {interests_str} experiences",
        f"things to do {spec.destination} {spec.budget_tier} budget",
        f"top rated restaurants {spec.destination}",
        f"{spec.destination} food tours and dining experiences"
    ]

    search_results = run_searches(search_queries, max_results_per_query=4, max_total=15)
    search_context = build_search_context(search_results, max_items=15)

    prompt = ChatPromptTemplate.from_template(
        ACTIVITIES_SYSTEM_PROMPT +
        "\n\nActivity Booking Tool Results:\n{activity_context}" +
        "\n\nAdditional Web Search Context:\n{search_context}"
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
        "activity_context": activity_context,
        "search_context": search_context
    })

    return {"activities_recommendations": response.content}
