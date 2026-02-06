# Vertex AI Setup Guide for Trip-Book

This guide will help you set up Google Cloud Vertex AI for the Trip-Book backend.

## Prerequisites
- Google Cloud account
- gcloud CLI installed
- Project ID: `My Project 27432` (or your project ID)

## Step-by-Step Setup

### 1. Enable Vertex AI API

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Select your project: `My Project 27432`
3. Navigate to: **APIs & Services → Library**
4. Search for "Vertex AI API"
5. Click **Enable**

### 2. Install Google Cloud CLI (if not installed)

**macOS:**
```bash
brew install google-cloud-sdk
```

**Or download from:** https://cloud.google.com/sdk/docs/install

Verify installation:
```bash
gcloud --version
```

### 3. Authenticate with Google Cloud

```bash
# Login to your Google account
gcloud auth login

# Set your project
gcloud config set project "My Project 27432"

# Create Application Default Credentials (ADC)
gcloud auth application-default login
```

This last command is **critical** - it creates local credentials that the application will use.

### 4. Set Environment Variables

Update your `backend/.env` file:

```bash
# Remove or comment out the old Gemini API key
# GEMINI_API_KEY=...

# Add Vertex AI configuration
GOOGLE_CLOUD_PROJECT=My Project 27432
GOOGLE_CLOUD_LOCATION=us-central1
```

**Available Regions:**
- `us-central1` (recommended - Iowa)
- `us-east1` (South Carolina)
- `us-west1` (Oregon)
- `europe-west1` (Belgium)
- `asia-northeast1` (Tokyo)

Choose the region closest to your users or yourself.

### 5. Verify Setup

Test that Vertex AI is accessible:

```bash
cd backend
python test_vertex.py
```

If you see "✓ Vertex AI is working!", you're all set!

## For Production (Service Account)

For deployment to servers or Docker, use a service account:

### 1. Create Service Account

```bash
gcloud iam service-accounts create trip-book-vertex \
    --display-name="Trip-Book Vertex AI Service Account"
```

### 2. Grant Vertex AI User Role

```bash
gcloud projects add-iam-policy-binding "My Project 27432" \
    --member="serviceAccount:trip-book-vertex@my-project-27432.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

### 3. Create JSON Key

```bash
gcloud iam service-accounts keys create vertex-key.json \
    --iam-account=trip-book-vertex@my-project-27432.iam.gserviceaccount.com
```

### 4. Use in Production

Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/vertex-key.json"
export GOOGLE_CLOUD_PROJECT="My Project 27432"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

**Security Note:** Never commit `vertex-key.json` to git! Add it to `.gitignore`.

## Available Models on Vertex AI

- `gemini-2.5-flash` - Latest, fastest (recommended)
- `gemini-2.5-pro` - More capable, slower
- `gemini-1.5-flash` - Stable, fast
- `gemini-1.5-pro` - Stable, capable

## Pricing

Vertex AI Gemini pricing (as of 2024):
- **gemini-2.5-flash**: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens
- Much cheaper than API key approach for production
- First 1M tokens per month are free

## Troubleshooting

### Error: "Project not found"
```bash
gcloud config set project "My Project 27432"
```

### Error: "Vertex AI API not enabled"
Enable it in Cloud Console or:
```bash
gcloud services enable aiplatform.googleapis.com
```

### Error: "Permission denied"
Make sure you ran:
```bash
gcloud auth application-default login
```

### Error: "Invalid region"
Check available regions:
```bash
gcloud ai models list --region=us-central1
```

## Cost Management

Set up budget alerts in Google Cloud Console:
1. Go to **Billing → Budgets & alerts**
2. Create budget with email notifications
3. Set threshold (e.g., $10/month)

## Next Steps

After setup:
1. Install new dependencies: `pip install -r requirements.txt`
2. Test Vertex connection: `python test_vertex.py`
3. Run agent tests: `python test_agents.py`
4. Start the application: `uvicorn app.main:app --reload`
