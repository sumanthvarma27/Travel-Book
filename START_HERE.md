# 🚀 START HERE - Trip-Book Setup

Welcome! Your Trip-Book application has been migrated to **Google Cloud Vertex AI** for production-ready AI capabilities.

## What You Have Now

✅ **7 AI Agents** with real-time web search (DuckDuckGo)
✅ **Vertex AI** integration (production-ready, secure)
✅ **Latest AI Model** (gemini-2.5-flash)
✅ **Beautiful UI** with 3D globe and animations
✅ **Complete Documentation**

## Quick Start (Choose One)

### Option A: Automated Setup (Easiest) ⚡

```bash
./setup_vertex.sh
```

This script does everything for you automatically.

### Option B: Manual Setup (5 minutes) 📝

1. **Install gcloud CLI** (if needed):
   ```bash
   brew install google-cloud-sdk
   ```

2. **Run these commands**:
   ```bash
   # Authenticate
   gcloud auth login

   # Set project
   gcloud config set project "My Project 27432"

   # Enable Vertex AI
   gcloud services enable aiplatform.googleapis.com

   # Create credentials
   gcloud auth application-default login
   ```

3. **Test connection**:
   ```bash
   cd backend
   python test_vertex.py
   ```

4. **Install dependencies** (if not done):
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Run the Application

Once setup is complete:

```bash
# Terminal 1 - Start Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Start Frontend
cd frontend
npm run dev
```

Visit: http://localhost:3000

## Test the System

### 1. Test Vertex AI Connection
```bash
cd backend
python test_vertex.py
```
Expected: `✅ Vertex AI is working correctly!`

### 2. Test All 7 AI Agents
```bash
python test_agents.py
```
Expected: All agents complete successfully with real data

### 3. Create a Test Trip
1. Go to http://localhost:3000
2. Click "Plan Your Journey"
3. Fill in: New York → Paris, June 1-5, 2 travelers
4. Wait 30-60 seconds
5. See personalized itinerary with real data!

## Documentation

| File | Purpose |
|------|---------|
| **START_HERE.md** | This file - quick start guide |
| **VERTEX_AI_SETUP.md** | Detailed Vertex AI setup instructions |
| **README_VERTEX.md** | Complete Vertex AI documentation |
| **VERTEX_MIGRATION_COMPLETE.md** | What changed in migration |
| **QUICKSTART.md** | Alternative quick start guide |
| **README.md** | General project documentation |

## What Each Component Does

### Backend (Python/FastAPI)
- 7 specialized AI agents
- Web search integration
- Weather forecasts
- LangGraph orchestration
- Vertex AI integration

### Frontend (Next.js)
- 3D globe landing page
- Trip wizard form
- Results display
- PDF/JSON export

### AI Agents
1. **Research** - Finds attractions and restaurants
2. **Weather** - Real-time forecasts
3. **Hotel** - Accommodation recommendations
4. **Logistics** - Flights and transport
5. **Activities** - Tours and experiences
6. **Budget** - Cost breakdowns
7. **Planner** - Orchestrates everything

## Environment Variables

Your `backend/.env` should have:

```bash
GOOGLE_CLOUD_PROJECT=My Project 27432
GOOGLE_CLOUD_LOCATION=us-central1
DATABASE_URL=sqlite:///./trips.db
LOG_LEVEL=INFO
```

## Common Issues & Solutions

### "gcloud not found"
```bash
brew install google-cloud-sdk
```

### "Permission denied"
```bash
gcloud auth application-default login
```

### "API not enabled"
```bash
gcloud services enable aiplatform.googleapis.com
```

### "Project not found"
```bash
gcloud config set project "My Project 27432"
```

### Port already in use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

## Project Structure

```
.
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── agents/         # 7 AI agents
│   │   ├── tools/          # Web search & weather
│   │   ├── graph/          # LangGraph workflow
│   │   └── schemas/        # Data models
│   ├── test_vertex.py      # Test Vertex AI
│   └── test_agents.py      # Test all agents
│
├── frontend/               # Next.js application
│   ├── app/               # Pages
│   ├── components/        # React components
│   └── lib/               # Utilities
│
├── setup_vertex.sh        # Automated setup
└── docs/                  # Documentation
```

## Cost Monitoring

Vertex AI usage costs approximately:
- **$0.01-$0.05 per trip**
- **$10-$50 for 1000 trips**
- **Free $300 credit** for new Google Cloud accounts

Set up budget alerts:
1. Go to https://console.cloud.google.com/billing
2. Create budget: $50/month
3. Enable email notifications

## Next Steps

1. ✅ Run `./setup_vertex.sh` (or manual setup)
2. ✅ Test with `python test_vertex.py`
3. ✅ Start backend: `uvicorn app.main:app --reload`
4. ✅ Start frontend: `npm run dev`
5. ✅ Create your first trip!
6. 🚀 Deploy to production

## Production Deployment

For deploying to servers:

1. Create service account key
2. Set `GOOGLE_APPLICATION_CREDENTIALS`
3. Use Docker or Cloud Run
4. See [VERTEX_AI_SETUP.md](VERTEX_AI_SETUP.md) for details

## Support

- **Setup Issues**: See VERTEX_AI_SETUP.md
- **Vertex AI Docs**: https://cloud.google.com/vertex-ai/docs
- **Pricing**: https://cloud.google.com/vertex-ai/pricing

## Success Checklist

Before you start building:

- [ ] gcloud CLI installed
- [ ] Authenticated with Google Cloud
- [ ] Vertex AI API enabled
- [ ] `test_vertex.py` passes
- [ ] `test_agents.py` passes
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can create a test trip successfully

Once all checked ✅, you're ready to build! 🎉

## What Makes This Special

🚀 **Production-Ready** - Vertex AI scales with your needs
🔒 **Secure** - No API keys to leak
💰 **Cost-Effective** - Pay only for what you use
🤖 **Latest AI** - Access to newest Gemini models
🌐 **Real Data** - Live web search and weather
🎨 **Beautiful UI** - Professional design

## Questions?

Read the documentation files in order:
1. START_HERE.md (this file)
2. VERTEX_AI_SETUP.md (if you need detailed setup)
3. README_VERTEX.md (for Vertex AI specifics)
4. VERTEX_MIGRATION_COMPLETE.md (for technical details)

**Ready? Run `./setup_vertex.sh` and let's go!** 🚀
