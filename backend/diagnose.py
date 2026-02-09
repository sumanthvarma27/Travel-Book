"""
Diagnostic script to test Trip-Book backend components.
Run this to identify what's broken.

Usage: python diagnose.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔍 TRIP-BOOK DIAGNOSTIC TOOL")
print("=" * 60)

# Test 1: Python version
print("\n1️⃣ Checking Python version...")
print(f"   Python: {sys.version}")
if sys.version_info < (3, 10):
    print("   ⚠️  WARNING: Python 3.10+ recommended")
else:
    print("   ✅ Python version OK")

# Test 2: Environment variables
print("\n2️⃣ Checking environment variables...")
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
    print(f"   ✅ GEMINI_API_KEY found: {masked_key}")
else:
    print("   ❌ GEMINI_API_KEY not found in .env")
    print("   Create backend/.env with: GEMINI_API_KEY=your_key_here")

# Test 3: Required packages
print("\n3️⃣ Checking required packages...")
required_packages = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("langchain_core", "LangChain Core"),
    ("langchain_google_genai", "LangChain Google GenAI"),
    ("langgraph", "LangGraph"),
    ("duckduckgo_search", "DuckDuckGo Search"),
    ("pydantic", "Pydantic"),
]

missing_packages = []
for package_name, display_name in required_packages:
    try:
        __import__(package_name)
        print(f"   ✅ {display_name}")
    except ImportError:
        print(f"   ❌ {display_name} NOT INSTALLED")
        missing_packages.append(package_name)

if missing_packages:
    print(f"\n   Install missing packages:")
    print(f"   pip install {' '.join(missing_packages)}")

# Test 4: LLM connection
print("\n4️⃣ Testing LLM connection...")
try:
    from app.core.llm import get_llm
    
    llm = get_llm(temperature=0.1, max_tokens=50)
    print("   ✅ LLM initialized")
    
    # Test actual API call
    try:
        response = llm.invoke("Say 'OK' if you can read this")
        print(f"   ✅ LLM API call successful: {response.content[:50]}")
    except Exception as e:
        print(f"   ❌ LLM API call failed: {str(e)[:100]}")
        
except Exception as e:
    print(f"   ❌ LLM initialization failed: {str(e)[:100]}")

# Test 5: Web search tool
print("\n5️⃣ Testing web search tool...")
try:
    from app.tools.web_search import web_search
    
    results = web_search("Paris travel guide", max_results=2)
    if results:
        print(f"   ✅ Web search working: Found {len(results)} results")
    else:
        print("   ⚠️  Web search returned no results")
        
except Exception as e:
    print(f"   ❌ Web search failed: {str(e)[:100]}")

# Test 6: Weather tool
print("\n6️⃣ Testing weather API...")
try:
    from app.tools.weather import weather_forecast, get_city_coordinates
    
    # Convert city name to coordinates
    lat, lon = get_city_coordinates("Paris")
    weather = weather_forecast(lat, lon, "2026-06-01", "2026-06-05")
    if "temperature" in weather.lower() or "forecast" in weather.lower():
        print(f"   ✅ Weather API working")
    else:
        print(f"   ⚠️  Weather API returned unexpected format")
        
except Exception as e:
    print(f"   ❌ Weather API failed: {str(e)[:100]}")

# Test 7: Agent imports
print("\n7️⃣ Testing agent imports...")
agents = [
    "research", "weather", "hotel", "budget", 
    "logistics", "activities", "planner"
]

for agent_name in agents:
    try:
        module = __import__(f"app.agents.{agent_name}", fromlist=[f"{agent_name}_node"])
        print(f"   ✅ {agent_name.capitalize()} agent")
    except Exception as e:
        print(f"   ❌ {agent_name.capitalize()} agent: {str(e)[:50]}")

# Test 8: Graph building
print("\n8️⃣ Testing graph construction...")
try:
    from app.graph.graph import build_graph
    
    graph = build_graph()
    print("   ✅ Graph built successfully")
    
except Exception as e:
    print(f"   ❌ Graph building failed: {str(e)[:100]}")

# Test 9: Schema validation
print("\n9️⃣ Testing schema definitions...")
try:
    from app.schemas.requests import TripSpec
    from app.schemas.itinerary import TripPlan, DayItinerary
    
    # Test creating a sample spec
    spec = TripSpec(
        origin="New York",
        destination="Paris",
        dates="2026-06-01 to 2026-06-05",
        travelers=2,
        budget_tier="medium",
        travel_style="pleasure",
        interests=["food", "museums"]
    )
    print("   ✅ TripSpec schema")
    print("   ✅ TripPlan schema")
    
except Exception as e:
    print(f"   ❌ Schema validation failed: {str(e)[:100]}")

# Test 10: Full workflow test
print("\n🔟 Testing full workflow (sample trip)...")
if not missing_packages and api_key:
    try:
        from app.graph.graph import build_graph
        from app.schemas.requests import TripSpec
        
        print("   Creating sample trip: NYC → Paris...")
        
        graph = build_graph()
        inputs = {
            "spec": TripSpec(
                origin="New York",
                destination="Paris",
                dates="2026-06-01 to 2026-06-05",
                travelers=2,
                budget_tier="medium",
                travel_style="pleasure",
                interests=["food"]
            ),
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
        
        print("   Running agents (this may take 30-60 seconds)...")
        import asyncio
        result = asyncio.run(graph.ainvoke(inputs))
        
        if result.get("plan"):
            print("   ✅ FULL WORKFLOW SUCCESSFUL!")
            print(f"   Plan title: {result['plan'].title}")
        else:
            print("   ⚠️  Workflow completed but no plan generated")
            print(f"   Status: {result.get('status')}")
            
    except Exception as e:
        print(f"   ❌ Workflow test failed: {str(e)[:200]}")
        import traceback
        print(f"\n   Full error:\n{traceback.format_exc()[:500]}")
else:
    print("   ⏭️  Skipping (missing dependencies or API key)")

# Summary
print("\n" + "=" * 60)
print("📋 DIAGNOSTIC SUMMARY")
print("=" * 60)

if not missing_packages and api_key:
    print("✅ All checks passed! Backend should work.")
    print("\nNext steps:")
    print("1. Start backend: uvicorn app.api.main:app --reload")
    print("2. Test endpoint: curl http://localhost:8000/health")
    print("3. Start frontend: cd ../frontend && npm run dev")
else:
    print("❌ Issues detected. Fix the errors above.")
    
print("\n")