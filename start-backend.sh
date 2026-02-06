#!/bin/bash

# Start Backend Server for AI Travel Planner

echo "🚀 Starting AI Travel Planner Backend..."
echo ""

cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "📝 Please edit backend/.env and add your GEMINI_API_KEY if you want LLM features"
    echo "   Or continue without it to use mock data"
    echo ""
fi

# Display API key status
if grep -q "GEMINI_API_KEY=.*[A-Za-z0-9]" .env 2>/dev/null; then
    echo "✅ GEMINI_API_KEY found - LLM features enabled"
else
    echo "⚠️  No GEMINI_API_KEY - Using mock data mode"
    echo "   To enable LLM: Set GEMINI_API_KEY in backend/.env"
fi

echo ""
echo "🌐 Backend will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "─────────────────────────────────────────────────"
echo ""

# Start the server
python run.py
