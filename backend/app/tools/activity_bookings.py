"""
Activity booking tool for finding tours and experiences with booking links.
"""

from langchain_core.tools import tool
from typing import Dict, Any, List
from app.tools.search_utils import web_search
import logging

logger = logging.getLogger(__name__)


@tool
def find_activity_bookings(
    destination: str,
    activities: List[str],
    max_results: int = 3
) -> Dict[str, Any]:
    """
    Find bookable activities and tours with direct booking links.
    
    Args:
        destination: City or location name
        activities: List of activity names/types to search for
        max_results: Maximum results per activity
    
    Returns:
        Dict with 'activities' list and 'platform_links' dict
    """
    try:
        dest_encoded = destination.replace(' ', '+')
        
        activity_results = []
        
        for activity in activities[:5]:  # Limit to 5 activities
            activity_encoded = activity.replace(' ', '+')
            search_query = f"{activity} {destination} tour booking"
            
            results = web_search(search_query, max_results=max_results)
            
            booking_options = []
            for result in results:
                # Determine platform from URL
                url = result.get("url", "")
                platform = "Other"
                if "viator.com" in url:
                    platform = "Viator"
                elif "getyourguide.com" in url:
                    platform = "GetYourGuide"
                elif "tripadvisor.com" in url:
                    platform = "TripAdvisor"
                elif "klook.com" in url:
                    platform = "Klook"
                
                booking_options.append({
                    "title": result.get("title", ""),
                    "platform": platform,
                    "url": url,
                    "snippet": result.get("snippet", "")
                })
            
            activity_results.append({
                "activity": activity,
                "booking_options": booking_options
            })
        
        # Generate platform landing pages
        platform_links = {
            "Viator": f"https://www.viator.com/searchResults/all?text={dest_encoded}",
            "GetYourGuide": f"https://www.getyourguide.com/s/?q={dest_encoded}",
            "TripAdvisor": f"https://www.tripadvisor.com/Attractions-{dest_encoded}",
            "Klook": f"https://www.klook.com/en-US/search/?query={dest_encoded}",
            "OpenTable": f"https://www.opentable.com/s?covers=2&term={dest_encoded}",
        }
        
        logger.info(f"✅ Found activities for {len(activities)} requests in {destination}")
        
        return {
            "activities": activity_results,
            "platform_links": platform_links,
            "destination": destination
        }
    
    except Exception as e:
        logger.error(f"❌ Activity search failed: {str(e)}")
        
        dest_encoded = destination.replace(' ', '+')
        return {
            "activities": [],
            "platform_links": {
                "Viator": f"https://www.viator.com/searchResults/all?text={dest_encoded}",
                "GetYourGuide": f"https://www.getyourguide.com/s/?q={dest_encoded}",
            },
            "destination": destination,
            "error": str(e)
        }