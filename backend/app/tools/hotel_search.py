"""
Hotel search tool for finding accommodations with booking platform links.
Based on reference implementation patterns.
"""

from langchain_core.tools import tool
from typing import Dict, Any, List
from .web_search import web_search_tool


@tool
def search_hotels(
    destination: str,
    checkin_date: str,
    checkout_date: str,
    num_guests: int = 2,
    budget_range: str = "Mid-Range"
) -> Dict[str, Any]:
    """
    Search for hotels using web search results and provide booking platform links.

    Args:
        destination: City or region to search for hotels
        checkin_date: Check-in date in YYYY-MM-DD format
        checkout_date: Check-out date in YYYY-MM-DD format
        num_guests: Number of guests
        budget_range: One of "Budget-Friendly", "Mid-Range", "Luxury"

    Returns:
        Dictionary containing hotel recommendations and booking platform links
    """
    try:
        # Build dynamic search query based on budget
        budget_terms = {
            "Budget-Friendly": "budget affordable cheap economical",
            "Mid-Range": "mid-range comfortable good value",
            "Luxury": "luxury boutique 5-star premium upscale"
        }
        budget_keywords = budget_terms.get(budget_range, "mid-range")

        # Perform web search
        query = f"{destination} {budget_keywords} hotels best rated {num_guests} guests 2026"

        search_results = web_search_tool.invoke({
            "query": query,
            "max_results": 6
        })

        # Extract and structure hotel results
        hotels = []
        for result in (search_results or [])[:6]:
            hotels.append({
                "name": result.get("title", ""),
                "description": (result.get("snippet", "") or "")[:250],
                "booking_url": result.get("url", ""),
                "source": "Web Search"
            })

        # Construct direct booking platform links
        destination_plus = destination.replace(" ", "+")
        destination_dash = destination.lower().replace(" ", "-")

        booking_platforms = {
            "Booking.com": f"https://www.booking.com/searchresults.html?ss={destination_plus}&checkin={checkin_date}&checkout={checkout_date}&group_adults={num_guests}",
            "Hotels.com": f"https://www.hotels.com/search.do?destination={destination_plus}&startDate={checkin_date}&endDate={checkout_date}&adults={num_guests}",
            "Airbnb": f"https://www.airbnb.com/s/{destination_dash}/homes?checkin={checkin_date}&checkout={checkout_date}&adults={num_guests}",
            "Expedia": f"https://www.expedia.com/Hotel-Search?destination={destination_plus}&startDate={checkin_date}&endDate={checkout_date}&rooms=1&adults={num_guests}",
            "Agoda": f"https://www.agoda.com/search?city={destination_plus}&checkIn={checkin_date}&checkOut={checkout_date}&rooms=1&adults={num_guests}"
        }

        return {
            "destination": destination,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "num_guests": num_guests,
            "budget_range": budget_range,
            "hotels": hotels,
            "booking_platforms": booking_platforms,
            "search_query": query
        }

    except Exception as e:
        return {
            "error": str(e),
            "destination": destination,
            "hotels": [],
            "booking_platforms": {}
        }
