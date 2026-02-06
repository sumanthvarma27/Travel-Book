from typing import TypedDict, List, Annotated, Optional
import operator
from langchain_core.messages import BaseMessage
from app.schemas.requests import TripSpec
from app.schemas.itinerary import TripPlan

class TripState(TypedDict):
    spec: TripSpec
    plan: Optional[TripPlan]
    messages: Annotated[List[BaseMessage], operator.add]
    research_notes: str
    weather_info: str
    hotel_recommendations: str
    budget_breakdown: str
    logistics_info: str
    activities_recommendations: str
    revision_count: int
    status: str
    plan_quality_score: int
