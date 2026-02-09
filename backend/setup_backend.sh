#!/bin/bash
# Trip-Book Backend Startup Script
# This ensures you always use the correct virtual environment

echo "🚀 Starting Trip-Book Backend..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Deactivate any active venv
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Deactivating current venv..."
    deactivate 2>/dev/null || true
fi

# Activate the correct venv
if [ -d ".venv312" ]; then
    echo "✅ Activating .venv312..."
    source .venv312/bin/activate
elif [ -d "venv" ]; then
    echo "⚠️  Using venv (you should use .venv312 instead)"
    source venv/bin/activate
else
    echo "❌ No virtual environment found!"
    echo "Run: python3 -m venv .venv312"
    exit 1
fi

# Check if we're in the right venv
if python -c "import langchain_google_genai" 2>/dev/null; then
    echo "✅ Packages found"
else
    echo "❌ langchain_google_genai not found in this venv"
    echo "Run: pip install -r requirements.txt"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Create backend/.env with your GEMINI_API_KEY"
fi

echo ""
echo "🚀 Starting backend server..."
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""

# Start the server
uvicorn app.api.main:app --reload