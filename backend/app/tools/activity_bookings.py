"""
Activity booking tool for finding tour and activity booking options.
Based on reference implementation patterns.
"""

from langchain_core.tools import tool
from typing import Dict, Any, List
from .web_search import web_search_tool


@tool
def find_activity_bookings(
    destination: str,
    activities: List[str],
    max_results: int = 3
) -> Dict[str, Any]:
    """
    Find booking options for activities in a destination.

    Args:
        destination: City or region where activities are located
        activities: List of activity names to search for
        max_results: Maximum search results per activity (default: 3)

    Returns:
        Dictionary containing activity booking options and platform links
    """
    try:
        platforms = ["Viator", "GetYourGuide", "TripAdvisor", "Klook", "Expedia"]
        activity_bookings = []

        # Limit to 5 activities to avoid rate limits
        for activity in activities[:5]:
            query = f"{activity} {destination} tickets booking tours"

            # Web search for each activity
            results = web_search_tool.invoke({
                "query": query,
                "max_results": max_results
            })

            booking_options = []
            for result in (results or []):
                url = (result.get("url", "") or "")
                url_lower = url.lower()

                # Detect which booking platform the URL belongs to
                platform_found = next(
                    (p for p in platforms if p.lower() in url_lower),
                    "Other"
                )

                booking_options.append({
                    "platform": platform_found,
                    "url": url,
                    "title": result.get("title", ""),
                    "snippet": (result.get("snippet", "") or "")[:250]
                })

            activity_bookings.append({
                "activity": activity,
                "booking_options": booking_options
            })

        # Add direct platform landing pages
        destination_plus = destination.replace(" ", "+")
        destination_dash = destination.lower().replace(" ", "-")

        platform_links = {
            "Viator": f"https://www.viator.com/{destination_dash}/d",
            "GetYourGuide": f"https://www.getyourguide.com/s/?q={destination_plus}",
            "TripAdvisor": f"https://www.tripadvisor.com/Search?q={destination_plus}",
            "Klook": f"https://www.klook.com/en-US/search/?query={destination_plus}",
            "Expedia Things To Do": f"https://www.expedia.com/things-to-do/search?location={destination_plus}"
        }

        return {
            "destination": destination,
            "activities": activity_bookings,
            "platform_links": platform_links,
            "total_activities": len(activity_bookings)
        }

    except Exception as e:
        return {
            "error": str(e),
            "destination": destination,
            "activities": [],
            "platform_links": {}
        }
