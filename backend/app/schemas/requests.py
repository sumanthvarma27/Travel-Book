"""
Request schemas for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class TripSpec(BaseModel):
    """Trip specification from user input"""
    
    origin: str = Field(..., description="Departure city")
    destination: str = Field(..., description="Destination city")
    dates: str = Field(..., description="Travel dates in format 'YYYY-MM-DD to YYYY-MM-DD'")
    travelers: int = Field(default=1, description="Number of travelers")
    budget_tier: str = Field(default="medium", description="Budget level: low, medium, high, luxury")
    travel_style: str = Field(default="pleasure", description="Trip type: pleasure, work, business")
    interests: List[str] = Field(default_factory=list, description="User interests (food, shopping, explore, heritage, relax, etc.)")
    constraints: List[str] = Field(default_factory=list, description="Any constraints or special requirements")
    
    class Config:
        json_schema_extra = {
            "example": {
                "origin": "New York",
                "destination": "Paris",
                "dates": "2026-06-01 to 2026-06-05",
                "travelers": 2,
                "budget_tier": "medium",
                "travel_style": "pleasure",
                "interests": ["food", "museums", "architecture"],
                "constraints": []
            }
        }