"""
Itinerary output schemas.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class WeatherData(BaseModel):
    """Weather information for a specific date"""
    date: str
    temperature_c: float
    condition: str
    precip_prob: Optional[int] = 0


class Activity(BaseModel):
    """Single activity or experience"""
    name: str
    description: str
    location: str
    estimated_cost: float
    booking_link: Optional[str] = None
    time_slot: str  # morning, afternoon, evening


class DailyPlan(BaseModel):
    """Itinerary for a single day"""
    day_number: int
    date: str
    city: str
    weather: Optional[WeatherData] = None
    morning_activities: List[Activity] = Field(default_factory=list)
    afternoon_activities: List[Activity] = Field(default_factory=list)
    evening_activities: List[Activity] = Field(default_factory=list)
    meal_suggestions: List[str] = Field(default_factory=list)


class AccommodationOption(BaseModel):
    """Hotel or accommodation recommendation"""
    name: str
    area: str
    price_per_night: float
    rating: Optional[float] = None
    description: str
    booking_link: Optional[str] = None


class TransportOption(BaseModel):
    """Transportation option (flight, train, bus, etc.)"""
    mode: str  # flight, train, bus, car
    provider: str
    departure: str
    arrival: str
    estimated_price: float
    booking_link: Optional[str] = None


class BudgetBreakdown(BaseModel):
    """Detailed budget breakdown"""
    flights: float
    accommodation: float
    activities: float
    food: float
    transport_local: float
    total_estimated: float
    currency: str = "USD"


class PackingItem(BaseModel):
    """Item for packing list"""
    category: str  # Clothing, Accessories, Documents, etc.
    item: str


class TripPlan(BaseModel):
    """Complete trip plan output"""
    title: str
    summary: str
    itinerary: List[DailyPlan]
    hotels_shortlist: List[AccommodationOption] = Field(default_factory=list)
    intercity_travel: List[TransportOption] = Field(default_factory=list)
    budget: BudgetBreakdown
    packing_list: List[PackingItem] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "5-Day Paris Adventure",
                "summary": "A romantic 5-day trip to Paris...",
                "itinerary": [],
                "hotels_shortlist": [],
                "intercity_travel": [],
                "budget": {
                    "flights": 600,
                    "accommodation": 500,
                    "activities": 250,
                    "food": 375,
                    "transport_local": 100,
                    "total_estimated": 1825,
                    "currency": "USD"
                },
                "packing_list": []
            }
        }


# Backwards-compatible alias: some modules expect `DayItinerary`
DayItinerary = DailyPlan
