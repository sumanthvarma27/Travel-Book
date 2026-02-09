"""
Mock data providers for testing without external APIs.
"""

from typing import List
from datetime import datetime, timedelta


class MockHotel:
    def __init__(self, name: str, area: str, price: float, rating: float, description: str):
        self.name = name
        self.area = area
        self.price_per_night = price
        self.rating = rating
        self.description = description
        self.booking_link = f"https://www.google.com/search?q={name.replace(' ', '+')}"


class MockFlight:
    def __init__(self, provider: str, departure: str, arrival: str, price: float):
        self.provider = provider
        self.departure = departure
        self.arrival = arrival
        self.estimated_price = price
        self.booking_link = f"https://www.google.com/flights?q={departure}+to+{arrival}"


class BookingMocks:
    """Mock booking data for when APIs are unavailable"""
    
    @staticmethod
    def search_hotels(destination: str, budget_tier: str) -> List[MockHotel]:
        """Generate mock hotel recommendations"""
        base_prices = {
            "low": 60,
            "medium": 120,
            "high": 250,
            "luxury": 500
        }
        base_price = base_prices.get(budget_tier, 120)
        
        return [
            MockHotel(
                name=f"Central {destination} Hotel",
                area="City Center",
                price=base_price,
                rating=4.2,
                description=f"Well-located hotel in the heart of {destination}"
            ),
            MockHotel(
                name=f"{destination} Boutique Stay",
                area="Downtown",
                price=base_price * 0.8,
                rating=4.5,
                description=f"Charming boutique accommodation"
            ),
            MockHotel(
                name=f"Budget Inn {destination}",
                area="Near Transit",
                price=base_price * 0.6,
                rating=3.8,
                description=f"Affordable option with good transport links"
            ),
        ]
    
    @staticmethod
    def search_flights(origin: str, destination: str, date: str) -> List[MockFlight]:
        """Generate mock flight options"""
        base_price = 300
        
        return [
            MockFlight(
                provider="Major Airline",
                departure=f"{origin} 08:00 AM",
                arrival=f"{destination} 02:30 PM",
                price=base_price
            ),
            MockFlight(
                provider="Budget Carrier",
                departure=f"{origin} 02:00 PM",
                arrival=f"{destination} 08:45 PM",
                price=base_price * 0.7
            ),
        ]