from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.requests import TripSpec
from app.schemas.itinerary import TripPlan
from app.graph.graph import build_graph
import uuid 
import asyncio

app = FastAPI(title="AI Travel Planner")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for MVP
trips_db = {}

graph_app = build_graph()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/plan")
async def create_plan(spec: TripSpec):
    run_id = str(uuid.uuid4())
    
    # Initialize state
    inputs = {
        "spec": spec,
        "revision_count": 0,
        "research_notes": "",
        "weather_info": "",
        "hotel_recommendations": "",
        "budget_breakdown": "",
        "logistics_info": "",
        "activities_recommendations": "",
        "plan_quality_score": 0,
        "messages": []
    }
    
    # Run graph
    # In production, use background tasks or a queue (Celery/Redis)
    # For MVP, we await it (might timeout on Vercel, but okay for local)
    try:
        result = await graph_app.ainvoke(inputs)
        plan = result.get("plan")
        if plan:
            trips_db[run_id] = plan
            return {"run_id": run_id, "status": "completed", "plan": plan}
        else:
             return {"run_id": run_id, "status": "failed", "error": "No plan generated"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trips/{run_id}")
def get_trip(run_id: str):
    if run_id not in trips_db:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trips_db[run_id]

@app.get("/trips")
def list_trips():
    return [{"id": k, "destination": v.itinerary[0].city if v.itinerary else "Unknown"} for k,v in trips_db.items()]
