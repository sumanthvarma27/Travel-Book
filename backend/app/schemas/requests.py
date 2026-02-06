from typing import List, Optional
from pydantic import BaseModel, Field

class TripSpec(BaseModel):
    origin: str
    destination: str
    dates: str = Field(..., description="Date range e.g. '2024-06-01 to 2024-06-10'")
    travelers: int = 1
    budget_tier: str = Field(..., description="low, medium, high, luxury")
    interests: List[str] = []
    constraints: List[str] = []
    travel_style: str = Field(..., description="pleasure, work, business, cultural, adventure")

    class Config:
        json_schema_extra = {
            "example": {
                "origin": "New York",
                "destination": "Tokyo",
                "dates": "2024-05-01 to 2024-05-07",
                "travelers": 2,
                "budget_tier": "medium",
                "interests": ["anime", "sushi", "history"],
                "constraints": ["no seafood"],
                "travel_style": "cultural"
            }
        }
