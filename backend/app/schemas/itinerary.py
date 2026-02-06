from typing import List, Optional
from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    date: str
    temperature_c: float
    condition: str
    precip_prob: int

class Activity(BaseModel):
    name: str
    description: str
    location: str
    estimated_cost: float
    booking_link: Optional[str] = None
    time_slot: str = Field(..., description="morning, afternoon, evening")

class DailyPlan(BaseModel):
    day_number: int
    date: str
    city: str
    weather: Optional[WeatherData] = None
    morning_activities: List[Activity] = []
    afternoon_activities: List[Activity] = []
    evening_activities: List[Activity] = []
    daily_transport_notes: Optional[str] = None
    meal_suggestions: List[str] = []

class AccommodationOption(BaseModel):
    name: str
    area: str
    price_per_night: float
    rating: Optional[float] = None
    booking_link: Optional[str] = None
    description: str

class TransportOption(BaseModel):
    type: str = Field(..., description="flight, train, bus, cab")
    provider: str
    departure: str
    arrival: str
    estimated_price: float
    booking_link: Optional[str] = None

class BudgetBreakdown(BaseModel):
    flights: float
    accommodation: float
    activities: float
    food: float
    transport_local: float
    total_estimated: float
    currency: str = "USD"

class PackingItem(BaseModel):
    category: str
    item: str
    reason: Optional[str] = None

class TripPlan(BaseModel):
    trip_id: Optional[str] = None
    title: str
    summary: str
    itinerary: List[DailyPlan]
    hotels_shortlist: List[AccommodationOption]
    intercity_travel: List[TransportOption]
    budget: BudgetBreakdown
    packing_list: List[PackingItem]
