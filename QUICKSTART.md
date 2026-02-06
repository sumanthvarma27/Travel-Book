# Quick Start Guide

Get Trip-Book running in 5 minutes!

## Prerequisites Check

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.10+ installed (`python --version`)
- [ ] Git installed

## Step 1: Get Gemini API Key (2 minutes)

1. Visit https://ai.google.dev/
2. Click "Get API Key in Google AI Studio"
3. Sign in with Google account
4. Create a new API key
5. Copy the key (starts with "AIza...")

## Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Install dependencies (already done if you see this file)
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_actual_key_here" > .env
# Replace 'your_actual_key_here' with your real key

# Test agents (optional but recommended)
python test_agents.py

# Start backend
uvicorn app.main:app --reload
```

Backend is now running at http://localhost:8000

## Step 3: Frontend Setup (1 minute)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies (if not done)
npm install

# Start frontend
npm run dev
```

Frontend is now running at http://localhost:3000

## Step 4: Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Plan Your Journey"
3. Fill in the form:
   - **From**: New York
   - **To**: Paris
   - **Start**: Any future date
   - **End**: 5 days later
   - **Travelers**: Couple
   - **Vibe**: Pleasure
   - **Budget**: Medium
   - **Interests**: Food, Museums
4. Click "Let's Go"
5. Wait 30-60 seconds for AI agents to plan your trip
6. View your personalized itinerary!

## What You Should See

✅ Loading animation for 30-60 seconds
✅ Detailed day-by-day itinerary
✅ Real weather forecasts
✅ Hotel recommendations with prices
✅ Flight options and local transport
✅ Activity suggestions with booking links
✅ Budget breakdown
✅ Packing suggestions

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is available
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

### Frontend won't start
```bash
# Check if port 3000 is available
lsof -i :3000
# Kill process if needed
kill -9 <PID>
```

### "No API key" error
- Check `.env` file exists in `backend/` directory
- Verify key starts with "AIza"
- No quotes around the key in .env file
- Restart backend after adding key

### "Web search failed" warnings
- This is normal - some searches may timeout
- Agents will use available data
- Check internet connection

### Slow response times
- First request always slower (model loading)
- Subsequent requests faster
- Normal time: 30-60 seconds per trip

## Quick Commands Reference

### Start Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Test Agents
```bash
cd backend
python test_agents.py
```

### View API Docs
http://localhost:8000/docs

### View Application
http://localhost:3000

## Optional: Add Video Background

1. Find a travel video (MP4 format)
2. Save as `frontend/public/videos/background.mp4`
3. Refresh page to see video background on wizard page

## Need Help?

1. Check `IMPLEMENTATION_SUMMARY.md` for technical details
2. Check `README.md` for full documentation
3. Check `INTEGRATION_PLAN.md` for implementation status
4. Review `backend/test_agents.py` for testing examples

## What's Next?

Once everything works:
- Try different destinations
- Experiment with budget tiers
- Test various interests
- Check the booking links
- Export itinerary as PDF/JSON (frontend feature)

Enjoy planning your trips with AI! 🌍✈️
