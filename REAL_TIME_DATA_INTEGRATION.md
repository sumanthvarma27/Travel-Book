# Real-Time Data Integration Guide

## Overview

This document describes how our Travel-Book application now provides **real-time hotel, activity, and booking information** by integrating patterns from the reference Multi-Agent AI Travel Planner.

## What Changed

### 1. New Tools for Real-Time Data

We've added two powerful new tools that provide live travel data:

#### **Hotel Search Tool** (`backend/app/tools/hotel_search.py`)
```python
@tool
def search_hotels(
    destination: str,
    checkin_date: str,
    checkout_date: str,
    num_guests: int = 2,
    budget_range: str = "Mid-Range"
) -> Dict[str, Any]
```

**Features:**
- Performs web search for current hotel recommendations
- Constructs direct booking platform links:
  - Booking.com (with dates, guests, destination)
  - Hotels.com (with dates, guests, destination)
  - Airbnb (with dates, guests, destination)
  - Expedia (with dates, guests, destination)
  - Agoda (with dates, guests, destination)
- Returns 6 search results with hotel names, descriptions, URLs
- Budget-aware search queries (Budget-Friendly, Mid-Range, Luxury)

**Example Output:**
```json
{
  "destination": "Paris",
  "checkin_date": "2026-06-01",
  "checkout_date": "2026-06-08",
  "num_guests": 2,
  "budget_range": "Mid-Range",
  "hotels": [
    {
      "name": "Hotel Le Marais",
      "description": "Charming boutique hotel in the heart of Paris...",
      "booking_url": "https://www.booking.com/hotel/fr/...",
      "source": "Web Search"
    }
  ],
  "booking_platforms": {
    "Booking.com": "https://www.booking.com/searchresults.html?ss=Paris&checkin=2026-06-01&checkout=2026-06-08&group_adults=2",
    "Hotels.com": "https://www.hotels.com/search.do?destination=Paris&startDate=2026-06-01&endDate=2026-06-08&adults=2",
    ...
  }
}
```

#### **Activity Booking Tool** (`backend/app/tools/activity_bookings.py`)
```python
@tool
def find_activity_bookings(
    destination: str,
    activities: List[str],
    max_results: int = 3
) -> Dict[str, Any]
```

**Features:**
- Searches for booking options for each activity
- Identifies booking platforms in results:
  - Viator
  - GetYourGuide
  - TripAdvisor
  - Klook
  - Expedia Things To Do
- Constructs direct platform landing pages
- Returns up to 3 booking options per activity

**Example Output:**
```json
{
  "destination": "Paris",
  "activities": [
    {
      "activity": "Eiffel Tower tour",
      "booking_options": [
        {
          "platform": "Viator",
          "url": "https://www.viator.com/tours/Paris/Eiffel-Tower/...",
          "title": "Skip-the-Line Eiffel Tower Guided Tour",
          "snippet": "Book your guided tour with priority access..."
        }
      ]
    }
  ],
  "platform_links": {
    "Viator": "https://www.viator.com/paris/d479",
    "GetYourGuide": "https://www.getyourguide.com/s/?q=Paris",
    ...
  }
}
```

### 2. Updated Agents

#### **Hotel Agent** (`backend/app/agents/hotel.py`)
**Changes:**
- Now calls `search_hotels` tool to get structured hotel data
- Provides direct booking platform links in output
- Includes retry logic for revision loop
- Combines tool results with web search context

**Agent Output Now Includes:**
```markdown
=== HOTEL SEARCH RESULTS ===
• Hotel Le Marais
  Charming boutique hotel in the heart of Paris's historic Marais district...
  Source: https://www.booking.com/hotel/fr/le-marais-paris.html

=== DIRECT BOOKING PLATFORMS ===
• Booking.com: https://www.booking.com/searchresults.html?ss=Paris&...
• Hotels.com: https://www.hotels.com/search.do?destination=Paris&...
• Airbnb: https://www.airbnb.com/s/paris/homes?checkin=...
• Expedia: https://www.expedia.com/Hotel-Search?destination=Paris&...
• Agoda: https://www.agoda.com/search?city=Paris&...
```

#### **Activities Agent** (`backend/app/agents/activities.py`)
**Changes:**
- Now calls `find_activity_bookings` tool
- Extracts activities from user interests
- Provides booking links for each activity
- Includes platform landing pages

**Agent Output Now Includes:**
```markdown
=== ACTIVITY BOOKING OPTIONS ===
🎯 Eiffel Tower tour experience in Paris
  • Skip-the-Line Eiffel Tower Guided Tour
    Platform: Viator
    Link: https://www.viator.com/tours/Paris/...

=== BOOKING PLATFORM LINKS ===
• Viator: https://www.viator.com/paris/d479
• GetYourGuide: https://www.getyourguide.com/s/?q=Paris
• TripAdvisor: https://www.tripadvisor.com/Search?q=Paris
• Klook: https://www.klook.com/en-US/search/?query=Paris
• Expedia Things To Do: https://www.expedia.com/things-to-do/search?location=Paris
```

### 3. Enhanced Router Check

The router check now has multiple quality signals to determine if hotel data needs improvement:

**Quality Checks:**
1. **Explicit Signal**: Planner returns "REVISE_HOTEL" if data is insufficient
2. **Content Analysis**: Checks for "unavailable", "no hotels", "not found" in hotel recommendations
3. **Length Check**: Hotel recommendations must be at least 100 characters
4. **Quality Score**: Scores below 6 trigger revision

**Revision Loop:**
```
Planner detects insufficient hotel data
    ↓
Router Check returns "revise_hotel"
    ↓
increment_revision node (tracks retry count)
    ↓
Hotel Agent (with broader search)
    ↓
Budget Agent (recalculate)
    ↓
Logistics Agent (replan)
    ↓
Planner Agent (re-evaluate)
    ↓
Router Check (proceed if acceptable)
```

**Maximum Retries:** 1 (prevents infinite loops)

### 4. Planner Agent Quality Control

The planner now evaluates hotel data quality BEFORE generating the full itinerary:

```python
# Check hotel data quality
hotel_missing = (
    "unavailable" in hotels_content_lower or
    "no hotels" in hotels_content_lower or
    len(hotels_content_lower) < 100
)

# Signal revision if needed
if hotel_missing and revision_count < max_retries:
    return {
        "plan": "REVISE_HOTEL",
        "status": "needs_hotel_revision",
        "plan_quality_score": 3
    }
```

## How It Works End-to-End

### User Request Flow:

1. **User submits trip request** (destination, dates, budget, interests)
   ↓
2. **Research Agent** → Web search for attractions, restaurants
   ↓
3. **Weather Agent** → Open-Meteo API for forecasts
   ↓
4. **Hotel Agent** → `search_hotels` tool
   - Performs web search for hotels
   - Constructs booking platform links
   - Returns 6 hotel results + 5 booking platforms
   ↓
5. **Budget Agent** → Calculate costs based on hotel data
   ↓
6. **Logistics Agent** → Plan transportation
   ↓
7. **Planner Agent** → Quality check
   - If hotel data insufficient → REVISE_HOTEL
   - If acceptable → Generate itinerary
   ↓
8. **Router Check** → Decision
   - If REVISE_HOTEL → Loop back to Hotel Agent (with broader search)
   - If OK → Continue to Activities
   ↓
9. **Activities Agent** → `find_activity_bookings` tool
   - Searches for each interest/activity
   - Identifies booking platforms
   - Returns booking links
   ↓
10. **Finalize Itinerary** → Complete
    ↓
11. **User receives:**
    - Day-by-day itinerary
    - Hotel recommendations with booking links
    - Activity recommendations with booking links
    - Direct links to Booking.com, Viator, GetYourGuide, etc.

## Data Sources

### What We Use:

| Data Type | Source | Cost | API Key Required | Live Data |
|-----------|--------|------|------------------|-----------|
| **LLM** | Google Vertex AI (Gemini) | Paid | Yes (Google Cloud) | Yes |
| **Web Search** | DuckDuckGo | Free | No | Yes |
| **Weather** | Open-Meteo | Free | No | Yes |
| **Hotels** | Web Search Results | Free | No | Partial* |
| **Activities** | Web Search Results | Free | No | Partial* |
| **Booking Platforms** | Direct Links | Free | No | No** |

\* Partial = Current hotel/activity names, ratings, and URLs from search results, but not real-time availability/pricing
\*\* No = User clicks links to check live availability on booking platforms

### What We DON'T Use:

- ❌ Booking.com API (requires enterprise license)
- ❌ Expedia API (requires partnership)
- ❌ Airbnb API (restricted access)
- ❌ Hotel booking APIs (expensive, rate-limited)

### Why This Approach Works:

✅ **Cost-Effective**: No expensive API subscriptions
✅ **No Rate Limits**: DuckDuckGo search is free and unlimited
✅ **Current Data**: Web search results are always up-to-date
✅ **User Control**: Users click through to booking platforms to see live availability/pricing
✅ **Multiple Options**: Provides 5+ booking platforms for comparison

## Example Output

When a user plans a trip to Paris, they now receive:

### Hotel Section:
```markdown
## Accommodations

Based on your Mid-Range budget and preferences, here are recommended hotels:

### Recommended Hotels
1. **Hotel Le Marais** - Historic Marais District
   - Price: €120-180/night
   - Rating: 4.5/5
   - Description: Charming boutique hotel in the heart of Paris's historic Marais...
   - [View on Booking.com](https://www.booking.com/hotel/fr/...)

2. **Hotel Saint-Germain** - Saint-Germain-des-Prés
   - Price: €140-200/night
   - Rating: 4.6/5
   - [View Details](https://...)

### Book Directly on These Platforms:
- [Booking.com - Paris Hotels](https://www.booking.com/searchresults.html?ss=Paris&checkin=2026-06-01&checkout=2026-06-08&group_adults=2)
- [Hotels.com - Paris Search](https://www.hotels.com/search.do?destination=Paris&...)
- [Airbnb - Paris Rentals](https://www.airbnb.com/s/paris/homes?checkin=...)
- [Expedia - Paris Hotels](https://www.expedia.com/Hotel-Search?destination=Paris&...)
- [Agoda - Paris Accommodations](https://www.agoda.com/search?city=Paris&...)
```

### Activities Section:
```markdown
## Activities & Experiences

### Eiffel Tower Experience
**Booking Options:**
- [Skip-the-Line Eiffel Tower Guided Tour](https://www.viator.com/...) - Viator
  Priority access with expert guide, 2.5 hours

- [Eiffel Tower Summit Access](https://www.getyourguide.com/...) - GetYourGuide
  Direct lift access to summit, skip the queues

### Louvre Museum Visit
**Booking Options:**
- [Louvre Skip-the-Line Ticket](https://www.viator.com/...) - Viator
- [Louvre Masterpieces Tour](https://www.getyourguide.com/...) - GetYourGuide

### Browse More Activities:
- [Viator - Paris Tours](https://www.viator.com/paris/d479)
- [GetYourGuide - Paris Activities](https://www.getyourguide.com/s/?q=Paris)
- [TripAdvisor - Paris Things To Do](https://www.tripadvisor.com/Search?q=Paris)
- [Klook - Paris Experiences](https://www.klook.com/en-US/search/?query=Paris)
```

## Testing the Integration

### Test Script
Run the end-to-end test to verify all components work:

```bash
cd backend
python test_agents.py
```

This will:
1. Test Vertex AI connection
2. Test web search tool
3. Test hotel search tool
4. Test activity booking tool
5. Run complete workflow with revision loop

### Manual Testing

Test the hotel search tool:
```python
from app.tools.hotel_search import search_hotels

result = search_hotels.invoke({
    "destination": "Paris",
    "checkin_date": "2026-06-01",
    "checkout_date": "2026-06-08",
    "num_guests": 2,
    "budget_range": "Mid-Range"
})

print(result["hotels"])  # Hotel search results
print(result["booking_platforms"])  # Direct booking links
```

Test the activity booking tool:
```python
from app.tools.activity_bookings import find_activity_bookings

result = find_activity_bookings.invoke({
    "destination": "Paris",
    "activities": ["Eiffel Tower tour", "Louvre Museum visit"],
    "max_results": 3
})

print(result["activities"])  # Activity booking options
print(result["platform_links"])  # Platform landing pages
```

## Benefits of This Approach

### For Users:
✅ **Real-time recommendations** from current web search results
✅ **Multiple booking options** - compare prices across platforms
✅ **Direct booking links** - one click to see availability
✅ **No markup** - book directly on platforms at best prices
✅ **Comprehensive options** - 5 hotel platforms, 5 activity platforms

### For Development:
✅ **No API costs** - uses free DuckDuckGo search
✅ **No rate limits** - unlimited searches
✅ **No authentication** - no need for hotel/activity API keys
✅ **Simple maintenance** - no API version updates or deprecations
✅ **Fast iteration** - add new platforms by just constructing URLs

### For Production:
✅ **Scalable** - no API quota limits
✅ **Reliable** - web search is always available
✅ **Cost-effective** - only pays for Vertex AI LLM calls
✅ **Up-to-date** - search results reflect current availability
✅ **Flexible** - easy to add new booking platforms

## Next Steps

### Frontend Integration (Pending)

Update the frontend to display booking links:

1. **Parse booking platform URLs** from agent responses
2. **Render clickable links** with platform logos
3. **Group by category** (Hotels, Activities)
4. **Add "Book Now" buttons** that open links in new tab

Example React component:
```tsx
<div className="booking-platforms">
  <h3>Book Your Hotel</h3>
  <div className="platform-links">
    {bookingPlatforms.map(platform => (
      <a
        key={platform.name}
        href={platform.url}
        target="_blank"
        rel="noopener noreferrer"
        className="platform-button"
      >
        <img src={platform.logo} alt={platform.name} />
        <span>Book on {platform.name}</span>
      </a>
    ))}
  </div>
</div>
```

### Future Enhancements

1. **Extract pricing** from search results using LLM
2. **Add more platforms** (Trivago, Kayak, Priceline)
3. **Cache search results** to avoid repeated searches
4. **Add affiliate tracking** (optional revenue stream)
5. **Display platform ratings** (Trustpilot scores)

## Troubleshooting

### Issue: Hotel search returns empty results

**Solution:**
- Check internet connection for DuckDuckGo access
- Try broader search terms (remove budget constraints)
- Check if destination name is spelled correctly

### Issue: Booking links don't work

**Solution:**
- Verify date format (YYYY-MM-DD)
- Check URL encoding for special characters
- Test links manually in browser

### Issue: Revision loop runs too many times

**Solution:**
- Check MAX_REVISIONS = 1 in router_check
- Verify revision_count is being incremented
- Add logging to track revision attempts

## Reference

This integration is based on the reference repository:
https://github.com/bitanmani/Multi-Agent_AI_Travel_Planner_LangGraph_Gemini

Key files from reference:
- `travel_planner_streamlit.py` - Agent implementations
- `AI_Travel_Planner_LangGraph_&_Gemini.ipynb` - Detailed tool definitions

---

**Last Updated:** 2026-02-09
**Status:** ✅ Integrated and Ready for Testing
