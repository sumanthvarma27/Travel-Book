#!/bin/bash

# Trip-Book Vertex AI Setup Script
# This script sets up Google Cloud Vertex AI for the Trip-Book backend

set -e  # Exit on error

echo "================================================"
echo "Trip-Book Vertex AI Setup"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}✗ gcloud CLI is not installed${NC}"
    echo ""
    echo "Please install gcloud CLI:"
    echo "  macOS: brew install google-cloud-sdk"
    echo "  Or visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✓ gcloud CLI found${NC}"

# Get project ID
PROJECT_ID="My Project 27432"
LOCATION="us-central1"

echo ""
echo "Configuration:"
echo "  Project: $PROJECT_ID"
echo "  Location: $LOCATION"
echo ""

# Step 1: Login
echo "Step 1: Authenticating with Google Cloud..."
echo "This will open a browser window for authentication."
read -p "Press Enter to continue..."
gcloud auth login

# Step 2: Set project
echo ""
echo "Step 2: Setting project..."
gcloud config set project "$PROJECT_ID"

# Step 3: Enable Vertex AI API
echo ""
echo "Step 3: Enabling Vertex AI API..."
gcloud services enable aiplatform.googleapis.com

# Step 4: Create Application Default Credentials
echo ""
echo "Step 4: Creating Application Default Credentials..."
echo "This will open another browser window."
read -p "Press Enter to continue..."
gcloud auth application-default login

# Step 5: Verify setup
echo ""
echo "Step 5: Verifying setup..."
if gcloud auth application-default print-access-token &> /dev/null; then
    echo -e "${GREEN}✓ ADC credentials are valid${NC}"
else
    echo -e "${RED}✗ ADC credentials failed${NC}"
    exit 1
fi

# Step 6: Update .env file
echo ""
echo "Step 6: Updating .env file..."
cd backend
if [ -f .env ]; then
    echo -e "${YELLOW}⚠ .env file exists, backing up to .env.backup${NC}"
    cp .env .env.backup
fi

cat > .env << EOF
# Vertex AI Configuration
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_LOCATION=$LOCATION

# Database
DATABASE_URL=sqlite:///./trips.db

# Logging
LOG_LEVEL=INFO
EOF

echo -e "${GREEN}✓ .env file updated${NC}"

# Step 7: Test connection
echo ""
echo "Step 7: Testing Vertex AI connection..."
python test_vertex.py

echo ""
echo "================================================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Start the backend: cd backend && uvicorn app.main:app --reload"
echo "2. Start the frontend: cd frontend && npm run dev"
echo "3. Visit http://localhost:3000"
echo ""
echo "To test agents: cd backend && python test_agents.py"
