# Troubleshooting Guide

## ✅ Issue Fixed: "Error generating plan"

**Problem:** When clicking "Generate Itinerary", you were getting an error message.

**Root Cause:** The planner agent was returning `None` when no GEMINI_API_KEY was set, instead of returning a proper mock plan.

**Solution:** ✅ FIXED! The planner now generates a complete mock plan even without an API key.

---

## Testing the Fix

Run this command to verify the backend is working:

```bash
./test-api.sh
```

You should see:
```
✅ Health check passed
✅ Plan generation successful!
✅ Get trip successful!
✅ List trips successful!
🎉 All API tests passed!
```

---

## Current Status

### ✅ Backend (Fully Working)
- All 7 agents implemented
- Cyclic workflow with quality control
- Real weather API integration
- **Mock mode working without API key**
- API tested and confirmed working

### ✅ Frontend (Ready)
- Should now work when you click "Generate Itinerary"
- Will receive mock plan data from backend
- Loading states should work properly

---

## How to Test the Full Application

### Step 1: Ensure Backend is Running
```bash
# In Terminal 1
./start-backend.sh
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Start Frontend
```bash
# In Terminal 2
./start-frontend.sh
```

You should see:
```
  ▲ Next.js 16.x.x
  - Local:        http://localhost:3000
```

### Step 3: Test in Browser
1. Open http://localhost:3000
2. Fill in the form:
   - **From:** New York
   - **To:** Paris
   - **Start Date:** March 15, 2026
   - **End Date:** March 22, 2026
   - **Budget:** Medium ($$)
   - **Style:** Cultural
   - **Interests:** Click on Art, Food, History
3. Click **"Generate Itinerary"**
4. Wait 5-10 seconds (mock mode is fast!)
5. You should see the trip plan!

---

## What You'll Get (Mock Mode)

### ✅ Complete Trip Plan Including:
- **Title:** "8-Day Paris Trip"
- **Summary:** Trip overview
- **Daily Itinerary:** 7 days with morning/afternoon/evening activities
- **Hotels:** Mock hotel recommendations
- **Budget:** Complete breakdown (~$2,560 for 2 travelers)
- **Packing List:** Essential items to bring

### Real Data You'll See:
- ✅ **Real Weather Forecast** from Open-Meteo API (not mock!)
- ✅ **Real City Coordinates** for 50+ cities
- Mock hotel, flight, and activity data

---

## Common Issues & Solutions

### Issue: Frontend shows "Failed to generate plan"

**Check:**
1. Is backend running? Visit http://localhost:8000/health
   - Should show: `{"status":"ok"}`

2. Check browser console (F12) for errors

3. Test backend directly:
   ```bash
   ./test-api.sh
   ```

**Solution:**
- If backend not running: `./start-backend.sh`
- If test fails: Check backend terminal for error messages

---

### Issue: "Connection refused" or "Network error"

**Cause:** Backend not running or wrong port

**Solution:**
1. Make sure backend is running on port 8000
2. Check if something else is using port 8000:
   ```bash
   lsof -ti:8000
   ```
3. If needed, kill the process:
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```
4. Restart backend: `./start-backend.sh`

---

### Issue: Frontend won't start

**Check:**
```bash
cd frontend
npm install
npm run dev
```

**If port 3000 is busy:**
```bash
lsof -ti:3000 | xargs kill -9
```

---

### Issue: Weather data not showing

**This should work automatically!** Weather API (Open-Meteo) is free and doesn't need a key.

**If it fails:**
- Check internet connection
- Weather API will fallback to generic recommendations
- Check backend terminal for weather-related errors

---

### Issue: Want to enable full LLM features

**Current:** Mock mode - Fast, works immediately, no API key needed

**To Enable LLM:**
1. Get Gemini API key: https://makersuite.google.com/app/apikey
2. Edit `backend/.env`:
   ```bash
   GEMINI_API_KEY=your-actual-key-here
   ```
3. Restart backend:
   ```bash
   # Stop with Ctrl+C
   ./start-backend.sh
   ```

**With LLM enabled, you get:**
- Real AI-powered destination research
- Intelligent hotel recommendations
- Personalized activity suggestions
- Comprehensive itineraries
- Takes 2-4 minutes instead of 5-10 seconds

---

## Verification Checklist

Use this checklist to verify everything is working:

- [ ] Backend health check passes: `curl http://localhost:8000/health`
- [ ] API test passes: `./test-api.sh`
- [ ] Backend running and showing logs
- [ ] Frontend running on http://localhost:3000
- [ ] Can access frontend in browser
- [ ] Can fill out trip form
- [ ] Can click "Generate Itinerary"
- [ ] Plan generates successfully (5-10 seconds)
- [ ] Can see trip details on results page

---

## Still Having Issues?

### 1. Check Backend Logs
Look at Terminal 1 (backend) for error messages

### 2. Check Frontend Console
Press F12 in browser, look at Console tab

### 3. Verify Dependencies
```bash
# Backend
cd backend
source venv/bin/activate
pip list | grep -E "(langchain|langgraph|openmeteo|fastapi)"

# Frontend
cd frontend
npm list next react
```

### 4. Clean Restart
```bash
# Stop both servers (Ctrl+C in both terminals)

# Backend
cd backend
rm -rf __pycache__ app/__pycache__
source venv/bin/activate
python run.py

# Frontend
cd frontend
rm -rf .next
npm run dev
```

---

## Performance Notes

### Mock Mode (Current):
- ⚡ Fast: 5-10 seconds
- ✅ No API key needed
- ✅ All agents return mock data
- ✅ Weather API still real (Open-Meteo)
- Perfect for testing UI and workflow

### LLM Mode (With API Key):
- 🐌 Slower: 2-4 minutes
- 🔑 Requires GEMINI_API_KEY
- 🤖 Real AI-powered planning
- 🎯 Production-quality results
- Better for actual trip planning

---

## Summary

**The error is now fixed!** 🎉

The planner was returning `None` when no API key was set. Now it generates a complete mock plan, so you can test the entire application without needing a Gemini API key.

**Next Steps:**
1. Start backend: `./start-backend.sh`
2. Start frontend: `./start-frontend.sh`
3. Open http://localhost:3000
4. Click "Generate Itinerary"
5. See your mock trip plan!

Everything should work now. If you still encounter issues, check the logs in both terminal windows for specific error messages.
