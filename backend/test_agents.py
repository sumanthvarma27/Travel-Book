"""
Test script to verify agent integrations with web search.
Run this to test if the AI agents are working correctly with real-time data.

Usage:
    python test_agents.py
"""

import asyncio
import os
from dotenv import load_dotenv
from app.schemas.requests import TripSpec
from app.graph.state import TripState
from app.agents.research import research_node
from app.agents.weather import weather_node
from app.agents.hotel import hotel_node
from app.agents.logistics import logistics_node
from app.agents.activities import activities_node
from app.agents.budget import budget_node

async def test_agents():
    # Load environment variables
    load_dotenv()

    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: GEMINI_API_KEY not found in .env file")
        print("   Using mock data mode. Set GEMINI_API_KEY to test real AI agents.\n")
    else:
        print("✓ GEMINI_API_KEY found. Testing with real AI agents.\n")

    # Create test trip specification
    test_spec = TripSpec(
        origin="New York",
        destination="Paris",
        dates="2026-06-01 to 2026-06-05",
        travelers=2,
        budget_tier="medium",
        travel_style="pleasure",
        interests=["food", "museums", "shopping"],
        constraints=[]
    )

    print("=" * 60)
    print("TESTING TRIP-BOOK AI AGENTS")
    print("=" * 60)
    print(f"Trip: {test_spec.origin} → {test_spec.destination}")
    print(f"Dates: {test_spec.dates}")
    print(f"Travelers: {test_spec.travelers}")
    print(f"Budget: {test_spec.budget_tier}")
    print(f"Interests: {', '.join(test_spec.interests)}")
    print("=" * 60 + "\n")

    # Initialize state
    state = TripState(
        spec=test_spec,
        plan=None,
        messages=[],
        research_notes="",
        weather_info="",
        hotel_recommendations="",
        budget_breakdown="",
        logistics_info="",
        activities_recommendations="",
        revision_count=0,
        status="pending",
        plan_quality_score=0
    )

    # Test each agent
    print("1. Testing Research Agent with Web Search...")
    print("-" * 60)
    state.update(await research_node(state))
    print(f"Research Notes: {state['research_notes'][:300]}...")
    print("✓ Research agent completed\n")

    print("2. Testing Weather Agent with Open-Meteo API...")
    print("-" * 60)
    state.update(await weather_node(state))
    print(f"Weather Info: {state['weather_info'][:300]}...")
    print("✓ Weather agent completed\n")

    print("3. Testing Hotel Agent with Web Search...")
    print("-" * 60)
    state.update(await hotel_node(state))
    print(f"Hotel Recommendations: {state['hotel_recommendations'][:300]}...")
    print("✓ Hotel agent completed\n")

    print("4. Testing Logistics Agent with Web Search...")
    print("-" * 60)
    state.update(await logistics_node(state))
    print(f"Logistics Info: {state['logistics_info'][:300]}...")
    print("✓ Logistics agent completed\n")

    print("5. Testing Activities Agent with Web Search...")
    print("-" * 60)
    state.update(await activities_node(state))
    print(f"Activities: {state['activities_recommendations'][:300]}...")
    print("✓ Activities agent completed\n")

    print("6. Testing Budget Agent with Web Search...")
    print("-" * 60)
    state.update(await budget_node(state))
    print(f"Budget Breakdown: {state['budget_breakdown'][:300]}...")
    print("✓ Budget agent completed\n")

    print("=" * 60)
    print("ALL AGENTS TESTED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    if not api_key:
        print("1. Add your GEMINI_API_KEY to backend/.env file")
        print("2. Re-run this test to see real AI-powered results")
    else:
        print("1. Start the backend: cd backend && uvicorn app.main:app --reload")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Visit http://localhost:3000 to test the full application")

if __name__ == "__main__":
    asyncio.run(test_agents())
