# Google Cloud Run Deployment (Free Tier)

## Why Google Cloud Run?
- 2 million requests per month FREE
- Pay only when used (perfect for testing)
- Auto-scales to zero (no idle costs)
- Supports up to 8GB memory

## Prerequisites
1. Google Cloud account (free $300 credit for new users)
2. Google Cloud SDK installed
3. Docker image ready

## Quick Deployment

### 1. Install Google Cloud SDK
```bash
# Windows (PowerShell)
# Download from: https://cloud.google.com/sdk/docs/install-windows
```

### 2. Build and Deploy
```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Build and deploy in one command
gcloud run deploy bana-tts \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --port 5000
```

### 3. Expected Output
```
✓ Building using Dockerfile
✓ Uploading sources
✓ Building Container
✓ Creating Revision
✓ Routing traffic
Done.
Service URL: https://bana-tts-xxxxxxxxx-uc.a.run.app
```

## Cost Estimation (Free Tier)
- **First 2M requests/month:** FREE
- **Memory:** 2GB-seconds per month FREE
- **CPU:** 1 vCPU-second per month FREE
- **For testing:** Completely free for months

## Configuration
Your app will automatically:
- Use PORT environment variable (already handled in app.py)
- Scale to zero when not used
- Auto-restart on requests
- Handle HTTPS automatically
