#!/bin/bash

# Start Frontend Server for AI Travel Planner

echo "🎨 Starting AI Travel Planner Frontend..."
echo ""

cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found!"
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "🌐 Frontend will be available at: http://localhost:3000"
echo ""
echo "Make sure backend is running at http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo "─────────────────────────────────────────────────"
echo ""

# Start the development server
npm run dev
