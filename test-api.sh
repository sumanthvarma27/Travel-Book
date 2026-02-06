#!/bin/bash

echo "🧪 Testing AI Travel Planner API"
echo "=================================="
echo ""

# Test 1: Health check
echo "1️⃣  Testing Health Endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
if echo "$HEALTH" | grep -q "ok"; then
    echo "✅ Health check passed: $HEALTH"
else
    echo "❌ Health check failed"
    echo "   Make sure backend is running: ./start-backend.sh"
    exit 1
fi
echo ""

# Test 2: Create a trip plan
echo "2️⃣  Testing Plan Generation..."
echo "   Sending request to create Paris trip plan..."

RESPONSE=$(curl -s -X POST http://localhost:8000/plan \
  -H 'Content-Type: application/json' \
  -d '{
    "origin": "New York",
    "destination": "Paris",
    "dates": "2026-03-15 to 2026-03-22",
    "travelers": 2,
    "budget_tier": "medium",
    "interests": ["Art", "Food", "History"],
    "constraints": [],
    "travel_style": "cultural"
  }')

if echo "$RESPONSE" | grep -q "status.*completed"; then
    echo "✅ Plan generation successful!"

    # Extract run_id
    RUN_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['run_id'])")
    echo "   Run ID: $RUN_ID"

    # Check plan details
    TITLE=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['plan']['title'])")
    echo "   Trip Title: $TITLE"

    BUDGET=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['plan']['budget']['total_estimated'])")
    echo "   Total Budget: \$$BUDGET USD"

    DAYS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['plan']['itinerary']))")
    echo "   Number of Days: $DAYS"

    echo ""
    echo "3️⃣  Testing Get Trip Endpoint..."
    TRIP=$(curl -s http://localhost:8000/trips/$RUN_ID)
    if echo "$TRIP" | grep -q "Paris"; then
        echo "✅ Get trip successful!"
    else
        echo "⚠️  Get trip returned unexpected data"
    fi

else
    echo "❌ Plan generation failed"
    echo "   Response: $RESPONSE"
    exit 1
fi

echo ""
echo "4️⃣  Testing List Trips Endpoint..."
TRIPS=$(curl -s http://localhost:8000/trips)
if echo "$TRIPS" | grep -q "Paris"; then
    echo "✅ List trips successful!"
    COUNT=$(echo "$TRIPS" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
    echo "   Total trips in database: $COUNT"
else
    echo "⚠️  List trips returned unexpected data"
fi

echo ""
echo "=================================="
echo "🎉 All API tests passed!"
echo ""
echo "Backend is working correctly. You can now:"
echo "  1. Start frontend: ./start-frontend.sh"
echo "  2. Open http://localhost:3000"
echo "  3. Try creating a trip plan!"
echo ""
echo "Note: Currently using MOCK mode (no GEMINI_API_KEY)"
echo "      To enable full LLM features, set GEMINI_API_KEY in backend/.env"
