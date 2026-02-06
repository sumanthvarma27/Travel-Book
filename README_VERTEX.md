# Trip-Book with Google Cloud Vertex AI

This version uses **Google Cloud Vertex AI** instead of the Gemini API key approach. Vertex AI is recommended for production use.

## Why Vertex AI?

✅ **Better rate limits** - Production-ready scaling
✅ **Lower costs** - More economical for high-volume usage
✅ **Enterprise features** - Better security, monitoring, and control
✅ **No API key leaks** - Uses Google Cloud authentication
✅ **Latest models** - Access to gemini-2.5-flash and newer models

## Quick Setup (5 minutes)

### Automated Setup
```bash
./setup_vertex.sh
```

This script will:
1. Authenticate with Google Cloud
2. Enable Vertex AI API
3. Set up credentials
4. Configure the backend
5. Test the connection

### Manual Setup

If you prefer to set up manually, see [VERTEX_AI_SETUP.md](./VERTEX_AI_SETUP.md) for detailed instructions.

## Prerequisites

1. **Google Cloud Account**: Free tier available
2. **Project ID**: `My Project 27432` (or create your own)
3. **gcloud CLI**: Install with `brew install google-cloud-sdk`

## Configuration

Your `backend/.env` file should look like:

```bash
# Vertex AI Configuration
GOOGLE_CLOUD_PROJECT=My Project 27432
GOOGLE_CLOUD_LOCATION=us-central1

# Database
DATABASE_URL=sqlite:///./trips.db
LOG_LEVEL=INFO
```

## Testing

### 1. Test Vertex AI Connection
```bash
cd backend
python test_vertex.py
```

You should see: `✅ Vertex AI is working correctly!`

### 2. Test All Agents
```bash
cd backend
python test_agents.py
```

This will test all 7 agents with real web search and Vertex AI.

### 3. Start the Application
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit http://localhost:3000

## Available Models

All agents now use **gemini-2.5-flash** by default:
- Fastest and most cost-effective
- Latest model with best performance
- Suitable for production

Alternative models you can use:
- `gemini-2.5-pro` - More capable, higher cost
- `gemini-1.5-flash` - Stable version
- `gemini-1.5-pro` - Stable, more capable

## Cost Estimates

With Vertex AI (approximate):
- **Per trip planning**: $0.01 - $0.05 USD
- **1000 trips/month**: ~$10 - $50 USD
- **Free tier**: First $300 credit for new accounts

Much more affordable than API key approach at scale!

## Architecture

```
User Request
     ↓
Frontend (Next.js)
     ↓
Backend (FastAPI)
     ↓
LangGraph Workflow
     ↓
7 AI Agents ──→ Vertex AI (gemini-2.5-flash)
     ↓             ↓
Web Search     Real-time AI
(DuckDuckGo)   Generation
     ↓
Weather API
(Open-Meteo)
     ↓
Complete Itinerary
```

## Troubleshooting

### "Project not found" error
```bash
gcloud config set project "My Project 27432"
```

### "API not enabled" error
```bash
gcloud services enable aiplatform.googleapis.com
```

### "Authentication failed" error
```bash
gcloud auth application-default login
```

### "Wrong region" error
Check available regions:
```bash
gcloud ai models list --region=us-central1
```

## Production Deployment

For production (Docker, Cloud Run, etc.), use a service account:

```bash
# Create service account
gcloud iam service-accounts create trip-book-vertex

# Grant permissions
gcloud projects add-iam-policy-binding "My Project 27432" \
  --member="serviceAccount:trip-book-vertex@my-project-27432.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Create key
gcloud iam service-accounts keys create vertex-key.json \
  --iam-account=trip-book-vertex@my-project-27432.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/vertex-key.json"
```

**Important**: Never commit `vertex-key.json` to git!

## Security Best Practices

1. ✅ Use service accounts for production
2. ✅ Enable least-privilege IAM roles
3. ✅ Set up budget alerts in Google Cloud
4. ✅ Monitor API usage and costs
5. ✅ Use VPC for sensitive deployments
6. ✅ Never commit credentials to git

## Monitoring

View usage and costs:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Vertex AI → Dashboard**
3. Check **Billing → Cost Breakdown**

Set up alerts:
1. **Billing → Budgets & alerts**
2. Create budget with email notifications
3. Set threshold (e.g., $50/month)

## Support

- **Vertex AI Setup**: See [VERTEX_AI_SETUP.md](./VERTEX_AI_SETUP.md)
- **API Documentation**: https://cloud.google.com/vertex-ai/docs
- **Pricing**: https://cloud.google.com/vertex-ai/pricing
- **Issues**: Open an issue on GitHub

## What Changed from API Key Version?

1. **Dependencies**: Now uses `langchain-google-vertexai` instead of `langchain-google-genai`
2. **Authentication**: Uses Google Cloud credentials (ADC) instead of API key
3. **Configuration**: Project ID + Location instead of API key
4. **All 7 agents**: Updated to use `ChatVertexAI` instead of `ChatGoogleGenerativeAI`
5. **Better production-ready**: Enterprise features and scaling

## Next Steps

1. ✅ Run `./setup_vertex.sh` to configure Vertex AI
2. ✅ Test with `python test_vertex.py`
3. ✅ Test agents with `python test_agents.py`
4. ✅ Start the application and create your first trip!
5. 🚀 Deploy to production with service account

Enjoy building with Vertex AI! 🎉
