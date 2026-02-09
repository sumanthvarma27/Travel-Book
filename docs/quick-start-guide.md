# Quick Start Guide: Multi-Agent Travel Planner

## Overview

Your AI Travel Planner now features 7 specialized agents with cyclic workflow and real weather integration!

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT (TripSpec)                     │
│  Origin, Destination, Dates, Budget, Interests, Style       │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATION                       │
│                                                              │
│  1. Weather Agent     → Real-time forecast (Open-Meteo)     │
│  2. Research Agent    → Destination info & attractions      │
│  3. Hotel Agent       → Accommodation recommendations       │
│  4. Logistics Agent   → Transportation planning             │
│  5. Budget Agent      → Cost breakdown & estimation         │
│  6. Activities Agent  → Tours, experiences, dining          │
│  7. Planner Agent     → Master itinerary synthesis          │
│                                                              │
│                     ↓ [Quality Check] ↓                      │
│                                                              │
│              Score ≥ 7?  →  YES → Output Plan               │
│                     ↓                                        │
│                    NO                                        │
│                     ↓                                        │
│         Revision < 2? → YES → Loop to Research              │
│                     ↓                                        │
│                    NO                                        │
│                     ↓                                        │
│              Output Best Available Plan                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Running the Application

### Backend Setup

```bash
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Set environment variable (optional, for LLM features)
export GEMINI_API_KEY="your-api-key-here"

# Run the server
python run.py
# Or:
uvicorn app.api.main:app --reload --port 8000
```

**Backend will be available at:** `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Run the development server
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

---

## Testing Without Gemini API Key

**Good news!** You can test the entire system without a Gemini API key. All agents have mock data fallbacks:

- **Weather Agent**: Uses real Open-Meteo API (free, no key needed)
- **Research Agent**: Returns simulated destination research
- **Hotel Agent**: Generates mock hotel options
- **Logistics Agent**: Returns mock flight and transport options
- **Budget Agent**: Calculates estimates based on budget tier
- **Activities Agent**: Generates booking platform search links
- **Planner Agent**: Returns basic mock plan (when no API key)

This allows you to test the workflow and UI immediately!

---

## Example API Request

### Create a Trip Plan

**Endpoint:** `POST http://localhost:8000/plan`

**Request Body:**
```json
{
  "origin": "New York",
  "destination": "Paris",
  "dates": "2026-03-15 to 2026-03-22",
  "travelers": 2,
  "budget_tier": "medium",
  "interests": ["Art", "Food", "History"],
  "constraints": [],
  "travel_style": "cultural"
}
```

**Response:**
```json
{
  "run_id": "abc123-def456-...",
  "status": "completed",
  "plan": {
    "trip_id": "...",
    "title": "7-Day Paris Cultural Experience",
    "summary": "...",
    "itinerary": [...],
    "hotels_shortlist": [...],
    "intercity_travel": [...],
    "budget": {...},
    "packing_list": [...]
  }
}
```

### Get Trip Plan

**Endpoint:** `GET http://localhost:8000/trips/{run_id}`

### List All Trips

**Endpoint:** `GET http://localhost:8000/trips`

---

## What Each Agent Does

### 1. Weather Agent 🌤️
- Fetches 7-16 day forecast from Open-Meteo
- Provides daily temperature, precipitation, wind, conditions
- Generates packing recommendations
- Covers 50+ major cities worldwide

**Output:** Detailed weather forecast with packing tips

### 2. Research Agent 🔍
- Discovers top activities, attractions, restaurants
- Matches with user interests
- Categorizes by time of day (morning/afternoon/evening)
- Provides local insights

**Output:** Comprehensive destination research notes

### 3. Hotel Agent 🏨
- Recommends 3-5 accommodation options
- Matches budget tier and travel style
- Considers location and amenities
- Provides booking links

**Output:** Hotel shortlist with prices and booking info

### 4. Logistics Agent ✈️
- Plans flights (outbound & return)
- Recommends local transportation
- Provides airport-to-hotel options
- Suggests transit passes and apps

**Output:** Complete transportation logistics plan

### 5. Budget Agent 💰
- Calculates total trip cost
- Breaks down by category (flights, hotel, food, activities, transport)
- Adjusts for budget tier and number of travelers
- Provides daily per-person budget

**Output:** Detailed budget breakdown in USD

### 6. Activities Agent 🎭
- Finds bookable tours and experiences
- Recommends attractions and dining
- Provides direct booking links (Viator, GetYourGuide, TripAdvisor, OpenTable)
- Organizes by time of day

**Output:** Curated activities with booking links

### 7. Planner Agent 📋
- Synthesizes all agent outputs
- Creates day-by-day itinerary
- Ensures logical flow and pacing
- Evaluates plan quality
- Requests revisions if needed (max 2)

**Output:** Structured JSON TripPlan

---

## Cyclic Workflow: How Quality Control Works

### Quality Evaluation

After the Planner generates a plan, it's automatically evaluated:

**Quality Score (0-10):**
- **8-10**: Excellent → Plan accepted immediately
- **7**: Good → Plan accepted
- **6 or below**: Needs improvement → Triggers revision

**Revision Logic:**
1. If quality score < 7 and revision_count < 2:
   - Increment revision counter
   - Loop back to Research Agent
   - Agents regenerate with improved context
2. If revision_count reaches 2:
   - Accept best available plan (prevents infinite loops)
3. If plan is None or score ≥ 7:
   - Finish and return plan

**Why This Matters:**
- Ensures minimum quality standards
- Automatically improves weak plans
- Prevents infinite loops with max revision limit
- Similar to reference project's quality control

---

## Supported Cities (Weather & Geocoding)

### North America
New York, Los Angeles, San Francisco, Chicago, Miami, Seattle, Boston, Washington DC, Toronto, Vancouver, Mexico City

### Europe
London, Paris, Rome, Barcelona, Amsterdam, Berlin, Madrid, Vienna, Prague, Istanbul, Athens, Lisbon, Dublin, Copenhagen, Stockholm, Oslo, Helsinki, Warsaw, Budapest, Zurich, Geneva, Brussels

### Asia
Tokyo, Kyoto, Osaka, Seoul, Beijing, Shanghai, Hong Kong, Singapore, Bangkok, Dubai, Mumbai, Delhi, Bangalore

### Oceania
Sydney, Melbourne, Auckland

### South America
Rio de Janeiro, São Paulo, Buenos Aires

### Africa
Cairo, Johannesburg

**Total:** 50+ cities

*Note: If your city isn't listed, the system defaults to New York coordinates. Consider adding new cities to `backend/app/tools/weather.py` → `get_city_coordinates()`*

---

## Budget Tiers

### Low Budget ($)
- **Daily budget:** ~$75 per person
- **Hotels:** Budget hostels, 2-star hotels
- **Food:** Local eateries, street food
- **Activities:** Free attractions, walking tours

### Medium Budget ($$)
- **Daily budget:** ~$150 per person
- **Hotels:** 3-star hotels, good Airbnbs
- **Food:** Mix of local and mid-range restaurants
- **Activities:** Paid attractions, some guided tours

### High Budget ($$$)
- **Daily budget:** ~$300 per person
- **Hotels:** 4-star hotels, boutique properties
- **Food:** Fine dining experiences
- **Activities:** Premium tours, skip-the-line passes

### Luxury ($$$$)
- **Daily budget:** $600+ per person
- **Hotels:** 5-star hotels, luxury resorts
- **Food:** Michelin-star dining
- **Activities:** Private tours, exclusive experiences

---

## Travel Styles

- **Relaxed**: Leisurely pace, plenty of downtime
- **Fast-paced**: Packed schedule, maximize sightseeing
- **Cultural**: Museums, history, local traditions
- **Foodie**: Culinary focus, cooking classes, food tours
- **Adventure**: Active experiences, outdoor activities

---

## Booking Platform Links

The system generates search links to:

- **Hotels**: Google Search (can upgrade to Booking.com API)
- **Flights**: Google Flights
- **Tours**: GetYourGuide, Viator
- **Attractions**: TripAdvisor
- **Dining**: OpenTable, TripAdvisor

*These are search links, not direct bookings. Future enhancement: integrate actual booking APIs*

---

## Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'openmeteo_requests'`
**Solution:**
```bash
cd backend
pip install openmeteo_requests requests_cache retry_requests
```

**Problem:** Weather API returns errors
**Solution:**
- Check internet connection
- Verify dates are in YYYY-MM-DD format
- Try a different city
- The system will fallback to generic recommendations

**Problem:** Planner returns None
**Solution:**
- Set GEMINI_API_KEY environment variable
- Or check that mock data is being generated
- Verify all agents are returning data

### Frontend Issues

**Problem:** CORS errors when calling backend
**Solution:**
- Backend already has CORS enabled for all origins
- Ensure backend is running on port 8000
- Check frontend API calls point to correct URL

**Problem:** Trip wizard not submitting
**Solution:**
- Check all required fields are filled
- Verify dates are selected
- Check browser console for errors

---

## Performance Expectations

### Execution Time
- **With LLM (Gemini API):** 2-4 minutes per plan
- **Mock mode (no API key):** 5-10 seconds per plan

### Agent Processing Time (Estimated)
- Weather: 1-3 seconds (API call)
- Research: 5-15 seconds (LLM)
- Hotel: 5-15 seconds (LLM)
- Logistics: 5-15 seconds (LLM)
- Budget: 3-8 seconds (LLM)
- Activities: 5-15 seconds (LLM)
- Planner: 15-30 seconds (LLM with complex JSON output)

### Revision Time
- Each revision adds ~60-90 seconds (re-runs Research → Planner)

---

## Environment Variables

```bash
# Required for LLM features (optional for testing)
GEMINI_API_KEY=your-api-key-here

# Future integrations (not yet implemented)
TAVILY_API_KEY=your-tavily-key-here
GOOGLE_MAPS_API_KEY=your-maps-key-here
VIATOR_API_KEY=your-viator-key-here
```

---

## Next Steps

### Immediate Actions:
1. **Start Backend:** `cd backend && python run.py`
2. **Start Frontend:** `cd frontend && npm run dev`
3. **Test with Mock Data:** Submit a trip without API key
4. **Test with Real LLM:** Set `GEMINI_API_KEY` and resubmit

### Try Different Scenarios:
- Different budget tiers (low vs luxury)
- Different travel styles (relaxed vs fast-paced)
- Different cities (Tokyo vs Paris vs New York)
- Different date ranges (3 days vs 14 days)
- Different interests (Art + Food vs Adventure + Nature)

### Future Enhancements:
1. Add real booking APIs (Booking.com, Expedia)
2. Implement real-time progress updates (WebSocket)
3. Add user authentication and trip history
4. Implement parallel agent execution
5. Add multi-city support
6. Build mobile app
7. Add PDF export
8. Implement collaborative trip planning

---

## Support & Resources

### Documentation
- `/docs/comparison-analysis.md` - Detailed comparison with reference project
- `/docs/implementation-summary.md` - Technical implementation details
- `README.md` - Project overview

### API Documentation
- Backend API docs: `http://localhost:8000/docs` (FastAPI auto-generated)
- Open-Meteo API: https://open-meteo.com/en/docs

### Code Structure
```
backend/
├── app/
│   ├── agents/          # 7 agent implementations
│   ├── api/             # FastAPI endpoints
│   ├── core/            # Prompts and config
│   ├── graph/           # LangGraph workflow
│   ├── schemas/         # Pydantic models
│   └── tools/           # Weather, mocks
├── run.py               # Server entry point
└── requirements.txt     # Python dependencies

frontend/
├── app/                 # Next.js pages
├── components/          # React components
├── lib/                 # API client, types
└── package.json         # Node dependencies
```

---

## Tips for Best Results

### 1. Be Specific with Interests
- ❌ "sightseeing"
- ✅ "Renaissance art", "Street food", "Hiking trails"

### 2. Realistic Date Ranges
- 3-7 days: Single city, relaxed
- 7-14 days: Single city deep-dive or 2-3 cities
- 14+ days: Multi-city adventure

### 3. Budget Alignment
- Ensure budget tier matches expectations
- Low budget won't include luxury hotels or Michelin dining
- Luxury tier expects premium experiences

### 4. Travel Style Consistency
- Pick style that matches your personality
- Fast-paced = 3-4 activities per day
- Relaxed = 1-2 activities + free time

### 5. Use Constraints Wisely
- Dietary restrictions: "vegetarian", "gluten-free"
- Physical limitations: "no hiking", "wheelchair accessible"
- Preferences: "avoid crowded places", "prefer local experiences"

---

## Feedback & Contributions

This is your project! Feel free to:
- Add more cities to weather database
- Enhance agent prompts
- Improve quality evaluation logic
- Add new agents (e.g., Packing Agent, Local Tips Agent)
- Integrate real booking APIs
- Build new features

The architecture is designed for easy extension. Happy building! 🚀

---

## Quick Reference: API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/plan` | Create new trip plan |
| GET | `/trips/{run_id}` | Get specific trip |
| GET | `/trips` | List all trips |

---

## Quick Reference: Budget Multipliers

| Tier | Daily Budget | Accommodation | Food | Activities | Transport |
|------|-------------|---------------|------|-----------|-----------|
| Low | $75 | 40% ($30) | 30% ($22.50) | 20% ($15) | 10% ($7.50) |
| Medium | $150 | 40% ($60) | 30% ($45) | 20% ($30) | 10% ($15) |
| High | $300 | 40% ($120) | 30% ($90) | 20% ($60) | 10% ($30) |
| Luxury | $600 | 40% ($240) | 30% ($180) | 20% ($120) | 10% ($60) |

*Plus flights (separate calculation based on origin-destination distance)*

---

🎉 **You're all set! Start planning amazing trips with AI!** 🌍✈️
