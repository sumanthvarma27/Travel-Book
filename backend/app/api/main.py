from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.requests import TripSpec
from app.schemas.itinerary import TripPlan
from app.graph.graph import build_graph
import uuid
from dotenv import load_dotenv
import traceback
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Travel Planner", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for MVP (use Redis/PostgreSQL in production)
trips_db = {}

# Build the LangGraph workflow once at startup
try:
    graph_app = build_graph()
    logger.info("✅ LangGraph workflow built successfully")
except Exception as e:
    logger.error(f"❌ Failed to build graph: {e}")
    graph_app = None


@app.get("/")
def root():
    """Health check and API info"""
    return {
        "message": "Trip-Book AI Travel Planner API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "plan": "POST /plan",
            "trips": "GET /trips",
            "trip_detail": "GET /trips/{run_id}"
        }
    }


@app.get("/health")
def health():
    """Detailed health check"""
    return {
        "status": "ok",
        "graph_initialized": graph_app is not None,
        "trips_count": len(trips_db)
    }


@app.post("/plan")
async def create_plan(spec: TripSpec):
    """
    Create a new trip plan using AI agents.
    
    This endpoint triggers the multi-agent workflow:
    Research → Weather → Hotel → Budget → Logistics → Planner → Activities
    """
    run_id = str(uuid.uuid4())
    
    if not graph_app:
        raise HTTPException(
            status_code=500,
            detail="Graph workflow not initialized. Check API key configuration."
        )
    
    logger.info(f"🚀 Starting trip planning for run_id: {run_id}")
    logger.info(f"📍 Destination: {spec.destination}, Dates: {spec.dates}")
    
    # Initialize state with all required fields
    inputs = {
        "spec": spec,
        "revision_count": 0,
        "research_notes": "",
        "weather_info": "",
        "hotel_recommendations": "",
        "budget_breakdown": "",
        "logistics_info": "",
        "activities_recommendations": "",
        "plan": None,
        "plan_quality_score": 0,
        "status": "started",
        "messages": []
    }
    
    try:
        # Execute the graph workflow
        logger.info("🔄 Invoking agent workflow...")
        result = await graph_app.ainvoke(inputs)
        
        # Extract the plan from results
        plan = result.get("plan")
        status = result.get("status", "unknown")
        
        logger.info(f"📊 Workflow completed with status: {status}")
        
        if plan:
            trips_db[run_id] = plan
            logger.info(f"✅ Plan generated successfully for run_id: {run_id}")
            return {
                "run_id": run_id,
                "status": "completed",
                "plan": plan
            }
        else:
            # Extract error details from state
            messages = result.get("messages", [])
            error_details = {
                "research_notes": result.get("research_notes", ""),
                "weather_info": result.get("weather_info", ""),
                "hotel_recommendations": result.get("hotel_recommendations", ""),
                "status": status
            }
            
            error_msg = "Plan generation failed"
            if messages:
                error_msg = f"{error_msg}: {'; '.join([str(m) for m in messages])}"
            
            logger.error(f"❌ Plan generation failed: {error_msg}")
            logger.error(f"State details: {error_details}")
            
            return {
                "run_id": run_id,
                "status": "failed",
                "error": error_msg,
                "details": error_details
            }
            
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"❌ Exception during plan generation: {str(e)}")
        logger.error(f"Traceback: {error_trace}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__,
                "run_id": run_id
            }
        )


@app.get("/trips/{run_id}")
def get_trip(run_id: str):
    """Get a specific trip by run_id"""
    if run_id not in trips_db:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {
        "run_id": run_id,
        "plan": trips_db[run_id]
    }


@app.get("/trips")
def list_trips():
    """List all generated trips"""
    return [
        {
            "id": k,
            "destination": v.itinerary[0].city if v.itinerary else "Unknown",
            "title": v.title if hasattr(v, 'title') else "Trip"
        }
        for k, v in trips_db.items()
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)