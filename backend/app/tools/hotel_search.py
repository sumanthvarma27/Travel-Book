"""
Hotel search tool for finding accommodations with booking links.
Uses web search to find hotels from major booking platforms.
"""

from langchain_core.tools import tool
from typing import Dict, Any, List
from app.tools.search_utils import web_search
import logging

logger = logging.getLogger(__name__)


@tool
def search_hotels(
    destination: str,
    checkin_date: str,
    checkout_date: str,
    num_guests: int = 2,
    budget_range: str = "medium"
) -> Dict[str, Any]:
    """
    Search for hotels using web search across major booking platforms.
    
    Args:
        destination: City or location name
        checkin_date: Check-in date (YYYY-MM-DD)
        checkout_date: Check-out date (YYYY-MM-DD)
        num_guests: Number of guests
        budget_range: Budget level (low/medium/high)
    
    Returns:
        Dict with 'hotels' list and 'booking_platforms' dict
    """
    try:
        # Prepare search queries for different booking platforms
        dest_encoded = destination.replace(' ', '+')
        
        # Search for hotel information
        search_query = f"best hotels {destination} {budget_range} budget {checkin_date}"
        search_results = web_search(search_query, max_results=8)
        
        # Extract hotel information from search results
        hotels = []
        for result in search_results[:5]:
            hotels.append({
                "name": result.get("title", "").replace(" - Booking.com", "").replace(" - Hotels.com", ""),
                "description": result.get("snippet", ""),
                "booking_url": result.get("url", "")
            })
        
        # Generate direct booking platform URLs
        booking_platforms = {
            "Booking.com": f"https://www.booking.com/searchresults.html?ss={dest_encoded}&checkin={checkin_date}&checkout={checkout_date}&group_adults={num_guests}",
            "Hotels.com": f"https://www.hotels.com/search.do?q-destination={dest_encoded}&q-check-in={checkin_date}&q-check-out={checkout_date}&q-rooms=1",
            "Airbnb": f"https://www.airbnb.com/s/{dest_encoded}/homes?checkin={checkin_date}&checkout={checkout_date}&adults={num_guests}",
            "Expedia": f"https://www.expedia.com/Hotel-Search?destination={dest_encoded}&startDate={checkin_date}&endDate={checkout_date}&rooms=1&adults={num_guests}",
        }
        
        logger.info(f"✅ Found {len(hotels)} hotel options for {destination}")
        
        return {
            "hotels": hotels,
            "booking_platforms": booking_platforms,
            "destination": destination,
            "dates": f"{checkin_date} to {checkout_date}"
        }
    
    except Exception as e:
        logger.error(f"❌ Hotel search failed: {str(e)}")
        
        # Fallback with platform links only
        dest_encoded = destination.replace(' ', '+')
        return {
            "hotels": [],
            "booking_platforms": {
                "Booking.com": f"https://www.booking.com/searchresults.html?ss={dest_encoded}",
                "Hotels.com": f"https://www.hotels.com/search.do?q-destination={dest_encoded}",
                "Airbnb": f"https://www.airbnb.com/s/{dest_encoded}/homes",
            },
            "destination": destination,
            "error": str(e)
        }