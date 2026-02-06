# Trip-Book Architecture

This document describes the multi-agent AI architecture for Trip-Book, matching the LangGraph workflow diagram.

## System Overview

Trip-Book uses **7 specialized AI agents** orchestrated by LangGraph to create personalized travel itineraries with real-time data.

## Agent Workflow

```
START (User Input: Destination, Dates, Budget, Interests)
  ↓
┌─────────────────┐
│ Research Agent  │ → web_search (DuckDuckGo) ← Find attractions, restaurants, hidden gems
└─────────────────┘
  ↓ State Object
┌─────────────────┐
│ Weather Agent   │ → weather_forecast (OpenWeather) ← Get 7-day forecast
└─────────────────┘
  ↓ State Object
┌─────────────────┐
│ Hotel Agent     │ → web_search (DuckDuckGo) ← Find accommodations
└─────────────────┘   search_hotels (Booking API)
  ↓ State Object
┌─────────────────┐
│ Budget Agent    │ → web_search (DuckDuckGo) ← Calculate costs
└─────────────────┘
  ↓ State Object
┌─────────────────┐
│ Logistics Agent │ → plan_multi_city (Routing Logic) ← Plan transportation
└─────────────────┘   web_search (DuckDuckGo)
  ↓ State Object
┌─────────────────┐
│ Planner Agent   │ ← Synthesizes all agent outputs (No Tools)
└─────────────────┘
  ↓ State Object
╔═════════════════╗
║  Router Check   ║ ← Quality evaluation
║ if quality < 6  ║
╚═════════════════╝
  ↓           ↓
  │           └──→ REVISE_HOTEL (loop back)
  │                   ↓
  │               increment_revision
  │                   ↓
  │               Hotel Agent → Budget → Logistics → Planner
  │
  ↓ (quality >= 6)
┌─────────────────┐
│ Activities Agent│ → find_activities (Local Events) ← Tours, experiences
└─────────────────┘   web_search (DuckDuckGo)
  ↓ State Object
┌──────────────────┐
│finalize_itinerary│ ← Format & Print Output
└──────────────────┘
  ↓
END (Complete Trip Plan)
```

## Agent Details

### 1. Research Agent
**Purpose**: Gathers information about destination attractions, restaurants, and local experiences

**Tools**:
- `web_search` (DuckDuckGo) - 4 queries:
  - Best things to do + interests
  - Top restaurants + budget tier
  - Hidden gems + local recommendations
  - Travel guide 2026

**Inputs**: destination, interests, budget_tier
**Outputs**: research_notes (text summary)
**Model**: gemini-2.5-flash via Vertex AI

### 2. Weather Agent
**Purpose**: Provides real-time weather forecasts for travel dates

**Tools**:
- `weather_forecast` (Open-Meteo API)
  - 7-day forecast
  - Temperature, conditions, precipitation
  - Packing recommendations

**Inputs**: destination, dates
**Outputs**: weather_info (detailed forecast)
**Model**: N/A (direct API call)

### 3. Hotel Agent
**Purpose**: Recommends accommodations matching budget and preferences

**Tools**:
- `web_search` (DuckDuckGo) - 3 queries:
  - Best hotels + budget tier 2026
  - Accommodation recommendations + travel style
  - Where to stay + travelers count
- `search_hotels` (Booking API) - Future enhancement

**Inputs**: destination, dates, budget_tier, travelers, interests, research_notes, weather_info
**Outputs**: hotel_recommendations (list with prices, links)
**Model**: gemini-2.5-flash via Vertex AI

### 4. Budget Agent
**Purpose**: Calculates detailed cost breakdown for entire trip

**Tools**:
- `web_search` (DuckDuckGo) - 4 queries:
  - Average cost of living + daily budget
  - Travel budget + budget tier
  - How much to visit destination
  - Food prices + restaurants 2026

**Inputs**: origin, destination, dates, travelers, budget_tier, research_notes, hotel_recommendations, logistics_info
**Outputs**: budget_breakdown (detailed costs in USD)
**Model**: gemini-2.5-flash via Vertex AI

### 5. Logistics Agent
**Purpose**: Plans transportation including flights and local transit

**Tools**:
- `web_search` (DuckDuckGo) - 4 queries:
  - Flights from origin to destination + date
  - Public transport in destination
  - Airport to city center transportation
  - Transportation tips + budget tier
- `plan_multi_city` (Routing Logic) - For multi-city trips

**Inputs**: origin, destination, dates, travelers, budget_tier, research_notes, weather_info
**Outputs**: logistics_info (flights, local transport options)
**Model**: gemini-2.5-flash via Vertex AI

### 6. Planner Agent (Synthesizer)
**Purpose**: Orchestrates all agent outputs into cohesive itinerary

**Tools**: None (pure synthesis)

**Inputs**: All previous agent outputs
- research_notes
- weather_info
- hotel_recommendations
- budget_breakdown
- logistics_info

**Outputs**:
- plan (TripPlan object)
- plan_quality_score (0-10)
- status

**Model**: gemini-2.5-flash via Vertex AI

**Quality Scoring**:
- 8-10: Excellent (complete data, logical flow)
- 6-7: Good (acceptable quality)
- 0-5: Needs improvement (triggers hotel revision)

### 7. Activities Agent
**Purpose**: Finds bookable tours, experiences, and dining

**Tools**:
- `web_search` (DuckDuckGo) - 5 queries:
  - Best tours and activities 2026
  - Destination + interests experiences
  - Things to do + budget tier
  - Top rated restaurants
  - Food tours and dining experiences
- `find_activities` (Local Events API) - Future enhancement

**Inputs**: destination, dates, travelers, budget_tier, interests, research_notes, weather_info, hotel_recommendations
**Outputs**: activities_recommendations (tours, restaurants with booking links)
**Model**: gemini-2.5-flash via Vertex AI

## State Management

The `TripState` object flows through all agents, accumulating information:

```python
class TripState(TypedDict):
    # Input
    spec: TripSpec

    # Agent Outputs
    research_notes: str
    weather_info: str
    hotel_recommendations: str
    budget_breakdown: str
    logistics_info: str
    activities_recommendations: str

    # Final Output
    plan: Optional[TripPlan]

    # Control Flow
    status: str
    plan_quality_score: int
    revision_count: int
    messages: List[BaseMessage]
```

## Router Logic

After the Planner Agent synthesizes the itinerary, the **Router Check** evaluates quality:

```python
def router_check(state: TripState) -> str:
    if revision_count >= MAX_REVISIONS:
        return "activities"  # Max retries reached

    if plan_quality_score < 6:
        return "revise_hotel"  # Loop back for better hotels

    return "activities"  # Good enough, continue
```

**Revision Loop**:
1. Planner → Router Check → increment_revision
2. Back to Hotel Agent (with context from previous iteration)
3. Hotel → Budget → Logistics → Planner
4. Router Check again (max 2 iterations)

## Data Flow

### Input (TripSpec)
```json
{
  "origin": "New York",
  "destination": "Paris",
  "dates": "2026-06-01 to 2026-06-05",
  "travelers": 2,
  "budget_tier": "medium",
  "travel_style": "pleasure",
  "interests": ["food", "museums"],
  "constraints": []
}
```

### Output (TripPlan)
```json
{
  "title": "5-Day Paris Trip",
  "summary": "A 5-day pleasure adventure...",
  "itinerary": [
    {
      "day_number": 1,
      "date": "2026-06-01",
      "city": "Paris",
      "weather": {"temp": 20, "condition": "Sunny"},
      "morning_activities": [...],
      "afternoon_activities": [...],
      "evening_activities": [...],
      "meal_suggestions": [...]
    }
  ],
  "hotels_shortlist": [...],
  "budget": {...},
  "packing_list": [...]
}
```

## Technology Stack

### AI & Orchestration
- **LangGraph**: Agent workflow orchestration
- **LangChain**: Agent prompting and chaining
- **Vertex AI**: Google Cloud's managed AI platform
- **Gemini 2.5 Flash**: Latest fast AI model

### Tools & APIs
- **DuckDuckGo Search**: Real-time web search
- **Open-Meteo API**: Weather forecasts
- **BeautifulSoup4**: HTML parsing (future)
- **Requests**: HTTP client

### Backend
- **FastAPI**: Python async web framework
- **Pydantic**: Data validation
- **SQLModel**: Database ORM

### Frontend
- **Next.js 16**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations

## Performance

### Timing (typical)
- Research Agent: ~8 seconds
- Weather Agent: ~2 seconds
- Hotel Agent: ~8 seconds
- Budget Agent: ~6 seconds
- Logistics Agent: ~8 seconds
- Planner Agent: ~8 seconds
- Activities Agent: ~10 seconds

**Total**: 30-60 seconds per trip

### API Calls (per trip)
- Web searches: ~20 queries
- Weather API: 1 call
- Vertex AI: 7 calls (one per agent)

### Costs (with Vertex AI)
- Per trip: ~$0.01-$0.05 USD
- 1000 trips/month: ~$10-$50 USD

## Error Handling

Each agent has fallback behavior:

1. **Web search fails**: Agent proceeds with available data
2. **API call fails**: Returns error in context
3. **No Vertex AI config**: Uses mock data
4. **Quality too low**: Router triggers revision (max 2 times)
5. **Max revisions**: Continues anyway to prevent infinite loops

## Scaling Considerations

### Current Architecture
- Sequential agent execution
- Synchronous workflow
- Single trip at a time

### Future Enhancements
- Parallel agent execution (where possible)
- Async processing with queues
- Caching for repeated queries
- Rate limiting and backoff
- Multi-trip batch processing

## Monitoring

Track these metrics in production:
- Agent execution times
- Quality scores distribution
- Revision frequency
- API call counts
- Error rates
- User satisfaction

## Diagram Legend

- **Blue boxes**: AI Agents with Vertex AI
- **Beige boxes**: Tool/API calls
- **Yellow diamond**: Router decision point
- **Pink oval**: End state
- **Dashed arrows**: Tool invocations
- **Solid arrows**: State flow
- **Red arrow**: Revision loop

This architecture ensures:
✅ Real-time data
✅ Quality control
✅ Self-correction
✅ Comprehensive planning
✅ Cost efficiency
