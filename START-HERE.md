# 🚀 Quick Start - AI Travel Planner

## Your Project is Ready to Run!

All dependencies are installed. You can start the application right now.

---

## Running the Application

### Option 1: Using the Startup Scripts (Recommended)

**Terminal 1 - Start Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
./start-frontend.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## Access the Application

Once both servers are running:

- **Frontend (User Interface):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## Testing the Application

### 1. Open Browser
Navigate to http://localhost:3000

### 2. Fill in the Trip Wizard:
- **From:** New York
- **To:** Paris
- **Dates:** Select any future dates (e.g., March 15-22, 2026)
- **Budget:** Medium ($$)
- **Style:** Cultural
- **Interests:** Select Art, Food, History

### 3. Click "Generate Itinerary"

The system will process through 7 specialized agents:
1. Weather Agent (3-5 seconds)
2. Research Agent (5-15 seconds)
3. Hotel Agent (5-15 seconds)
4. Logistics Agent (5-15 seconds)
5. Budget Agent (3-8 seconds)
6. Activities Agent (5-15 seconds)
7. Planner Agent (15-30 seconds)

**Total time:** 2-4 minutes with LLM, 5-10 seconds in mock mode

---

## Current Mode

### Without GEMINI_API_KEY (Mock Mode)
✅ **Ready to test immediately!**

The application will use mock data:
- ✅ Real weather from Open-Meteo API
- ✅ Mock hotels with realistic pricing
- ✅ Mock flights and transportation
- ✅ Mock budget calculations
- ✅ Mock activities with booking platform links
- ✅ Basic itinerary structure

This is perfect for testing the UI and workflow!

### With GEMINI_API_KEY (Full LLM Mode)
🎯 **For production-quality travel plans**

To enable LLM features:
1. Get a Gemini API key from https://makersuite.google.com/app/apikey
2. Edit `backend/.env`
3. Set: `GEMINI_API_KEY=your-key-here`
4. Restart backend server

With LLM enabled, you get:
- 🤖 AI-powered destination research
- 🏨 Intelligent hotel recommendations
- 💰 Smart budget analysis
- 🎭 Personalized activity suggestions
- 📋 Comprehensive day-by-day itineraries

---

## What You'll See

### 1. Trip Wizard Form (Home Page)
- Beautiful glassmorphism design
- Step-by-step form inputs
- Interest tag selection
- Date pickers and budget selectors

### 2. Loading State
- Animated spinner
- "Consulting AI Agents..." message
- Status indicators (in future: shows which agent is running)

### 3. Results Page
- Trip plan overview
- Day-by-day itinerary
- Hotel recommendations
- Budget breakdown
- Activities with booking links
- Weather forecast

---

## System Architecture

```
User Input → Frontend (Next.js)
                ↓
         Backend API (FastAPI)
                ↓
         LangGraph Workflow
                ↓
    ┌──────────────────────┐
    │   7 Specialized      │
    │      Agents          │
    ├──────────────────────┤
    │ 1. Weather          │ ← Open-Meteo API
    │ 2. Research         │ ← Gemini LLM
    │ 3. Hotel            │ ← Gemini LLM
    │ 4. Logistics        │ ← Gemini LLM
    │ 5. Budget           │ ← Gemini LLM
    │ 6. Activities       │ ← Gemini LLM
    │ 7. Planner          │ ← Gemini LLM
    └──────────────────────┘
                ↓
        Quality Check
                ↓
    Score ≥ 7? → Yes → Output
                ↓
               No
                ↓
    Revisions < 2? → Yes → Loop Back
                ↓
               No
                ↓
         Best Available Plan
```

---

## Stopping the Servers

Press `Ctrl + C` in each terminal window to stop the servers.

---

## Troubleshooting

### Backend won't start?
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Frontend won't start?
```bash
cd frontend
npm install
npm run dev
```

### Port already in use?
- Backend: Kill process on port 8000
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```
- Frontend: Kill process on port 3000
  ```bash
  lsof -ti:3000 | xargs kill -9
  ```

### Can't see weather data?
- Check internet connection
- Weather API (Open-Meteo) is free and doesn't need a key
- System will fallback to general recommendations if API fails

---

## Features Implemented ✅

- ✅ 7 Specialized Agents (Weather, Research, Hotel, Budget, Logistics, Activities, Planner)
- ✅ Cyclic Workflow with Quality Control (max 2 revisions)
- ✅ Real Weather API Integration (Open-Meteo)
- ✅ 50+ Cities with Coordinates
- ✅ Mock Data Mode (works without API key)
- ✅ Beautiful Glassmorphism UI
- ✅ Budget Tiers (Low, Medium, High, Luxury)
- ✅ Travel Styles (Relaxed, Fast-paced, Cultural, Foodie, Adventure)
- ✅ Interest-based Recommendations
- ✅ Booking Platform Links (Viator, GetYourGuide, TripAdvisor, OpenTable)
- ✅ Daily Weather Forecasts with Packing Tips
- ✅ Comprehensive Budget Breakdown

---

## Next Steps After Testing

1. **Add Your Gemini API Key** for full LLM features
2. **Try Different Scenarios:**
   - Different cities (Tokyo, London, Barcelona)
   - Different budget tiers
   - Different travel styles
   - Different date ranges

3. **Explore the Code:**
   - `backend/app/agents/` - See how each agent works
   - `backend/app/graph/graph.py` - Understand the workflow
   - `frontend/components/` - Check out the UI components

4. **Extend the Project:**
   - Add more cities to weather database
   - Enhance agent prompts
   - Add real booking APIs
   - Implement WebSocket for real-time progress
   - Add user authentication
   - Build mobile app

---

## Documentation

- 📖 `docs/quick-start-guide.md` - Detailed usage guide
- 📊 `docs/comparison-analysis.md` - Comparison with reference project
- 🔧 `docs/implementation-summary.md` - Technical implementation details
- 📚 `README.md` - Project overview

---

## API Testing (Optional)

You can test the backend API directly using curl or Postman:

```bash
# Health check
curl http://localhost:8000/health

# Create a trip plan
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "New York",
    "destination": "Paris",
    "dates": "2026-03-15 to 2026-03-22",
    "travelers": 2,
    "budget_tier": "medium",
    "interests": ["Art", "Food", "History"],
    "constraints": [],
    "travel_style": "cultural"
  }'

# List all trips
curl http://localhost:8000/trips

# Get specific trip (replace {run_id} with actual ID)
curl http://localhost:8000/trips/{run_id}
```

---

## Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Verify both servers are running
3. Check browser console for frontend errors
4. Review the troubleshooting section above
5. Check the documentation in `/docs`

---

## Summary

**You're all set!** 🎉

1. Run `./start-backend.sh` in one terminal
2. Run `./start-frontend.sh` in another terminal
3. Open http://localhost:3000 in your browser
4. Start planning amazing trips!

The system is fully functional in mock mode. Add your Gemini API key when you're ready for production-quality AI-powered travel planning.

**Happy traveling!** 🌍✈️
