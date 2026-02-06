from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: str = Field(index=True)
    destination: str
    plan_json: str # Storing the full JSON blob simplified
    created_at: datetime = Field(default_factory=datetime.utcnow)
