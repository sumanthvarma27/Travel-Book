# Trip-Book - AI-Powered Travel Planning

An intelligent travel planning application powered by 7 specialized AI agents that work together to create personalized trip itineraries with real-time data.

## Features

- **7 Specialized AI Agents**:
  - Research Agent: Finds attractions, restaurants, and hidden gems
  - Weather Agent: Real-time weather forecasts via Open-Meteo API
  - Hotel Agent: Accommodation recommendations with web search
  - Budget Agent: Detailed cost breakdowns and estimates
  - Logistics Agent: Flight and transportation planning
  - Activities Agent: Bookable tours and experiences
  - Planner Agent: Orchestrates everything into a complete itinerary

- **Real-Time Data**:
  - Web search powered by DuckDuckGo
  - Live weather forecasts
  - Current pricing and availability information
  - 2026-ready recommendations

- **Beautiful UI**:
  - Interactive 3D globe landing page
  - Glass morphism design with video backgrounds
  - Responsive wizard form for trip planning
  - Detailed results with booking links

## Tech Stack

### Frontend
- Next.js 16 with App Router
- React Three Fiber for 3D graphics
- Framer Motion for animations
- TypeScript
- Tailwind CSS

### Backend
- FastAPI (Python)
- LangGraph for agent orchestration
- LangChain + Google Gemini 2.0 Flash
- DuckDuckGo Search API
- Open-Meteo Weather API

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Google Gemini API Key (get from https://ai.google.dev/)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in backend directory:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Test the agents (optional):
```bash
python test_agents.py
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) Add video background:
   - Place your video files in `frontend/public/videos/`
   - Supported formats: `.mp4`, `.webm`
   - Name: `background.mp4` or `background.webm`

4. Start the development server:
```bash
npm run dev
```

Frontend will run at `http://localhost:3000`

## Usage

1. Visit `http://localhost:3000` in your browser
2. Click "Plan Your Journey" button
3. Fill in the trip wizard:
   - Origin and destination cities
   - Travel dates
   - Number of travelers
   - Budget tier (Low/Medium/High)
   - Travel vibe (Pleasure/Work/Business)
   - Interests (Food, Shopping, Explore, Heritage, Relax)
4. Click "Let's Go" to generate your personalized itinerary
5. View detailed results with:
   - Day-by-day activities
   - Flight recommendations
   - Hotel options with booking links
   - Local transportation tips
   - Weather forecasts
   - Budget breakdown
   - Packing suggestions

## Project Structure

```
.
├── frontend/               # Next.js application
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/              # Utilities and API client
│   └── public/           # Static assets
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── agents/       # 7 AI agent implementations
│   │   ├── graph/        # LangGraph workflow
│   │   ├── tools/        # Web search and weather tools
│   │   ├── core/         # Prompts and config
│   │   └── schemas/      # Pydantic models
│   └── test_agents.py    # Agent testing script
├── docs/                  # Documentation
└── INTEGRATION_PLAN.md   # Implementation details
```

## API Key Configuration

### Getting a Gemini API Key
1. Visit https://ai.google.dev/
2. Click "Get API Key in Google AI Studio"
3. Create a new API key
4. Copy the key and add it to `backend/.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

### Running Without API Key
The application includes fallback mock data for testing without an API key. However, you won't get:
- Real-time web search results
- AI-powered recommendations
- Personalized itineraries

## Development

### Testing Agents
```bash
cd backend
python test_agents.py
```

This will test all 7 agents and show their outputs. Use this to verify:
- Web search is working
- Weather API is connected
- Gemini API key is valid
- Agents are producing real data

### API Endpoints
- `POST /plan` - Create a new trip plan
- `GET /health` - Health check
- Full API docs at `http://localhost:8000/docs`

## Features Implemented

✅ Frontend with 3D globe and wizard
✅ 7 specialized AI agents
✅ Web search integration (DuckDuckGo)
✅ Real weather forecasts (Open-Meteo)
✅ LangGraph multi-agent workflow
✅ Gemini 2.0 Flash integration
✅ Mock data fallback mode
✅ Responsive design
✅ Video backgrounds
✅ Booking link generation

## Contributing

This is a personal project. Feel free to fork and modify for your own use.

## License

MIT License
