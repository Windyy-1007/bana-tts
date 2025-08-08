# Bana TTS - Deployment Guide

This guide explains how to deploy your Bana TTS application to various hosting platforms.

## Prerequisites

- Docker installed on your system
- Your application is already containerized (Dockerfile exists)
- Model checkpoints are available in the `checkpts/` directory

## Quick Local Deployment

```bash
# Using Docker Compose (recommended for local testing)
docker-compose up -d

# Or using Docker directly
docker build -t bana-tts .
docker run -p 5000:5000 bana-tts
```

Your app will be available at `http://localhost:5000`

## Cloud Hosting Options

### 1. Railway (Easiest) 🌟

**Cost:** $5/month starter plan  
**Setup time:** 5 minutes

1. Push your code to GitHub
2. Go to [Railway](https://railway.app)
3. Connect your GitHub repo
4. Railway automatically detects the Dockerfile and deploys
5. Get a public URL instantly

### 2. DigitalOcean App Platform

**Cost:** $5-12/month  
**Setup time:** 10 minutes

1. Push code to GitHub
2. Go to DigitalOcean App Platform
3. Connect GitHub repository
4. Configure:
   - Environment: Docker
   - Port: 5000
   - Instance size: Basic ($5/month)
5. Deploy

### 3. Google Cloud Run (Pay-per-use)

**Cost:** Pay only when used (~$0-10/month)  
**Setup time:** 15 minutes

```bash
# Install gcloud CLI first
gcloud builds submit --tag gcr.io/PROJECT-ID/bana-tts
gcloud run deploy bana-tts \
  --image gcr.io/PROJECT-ID/bana-tts \
  --platform managed \
  --port 5000 \
  --memory 2Gi \
  --cpu 1 \
  --allow-unauthenticated
```

### 4. Heroku Container Registry

**Cost:** $7/month (Hobby plan)  
**Setup time:** 10 minutes

```bash
heroku login
heroku container:login
heroku create your-app-name
heroku container:push web
heroku container:release web
```

### 5. AWS ECS/Fargate

**Cost:** $10-30/month  
**Setup time:** 30 minutes

More complex setup involving ECR, ECS, and Load Balancer configuration.

### 6. VPS Deployment (Most Control)

**Cost:** $5-20/month  
**Setup time:** 20 minutes

For Ubuntu/CentOS servers:

```bash
# Copy files to server
scp docker-compose.yml user@your-server:/home/user/
scp -r . user@your-server:/home/user/bana-tts/

# On server
cd /home/user/bana-tts
docker-compose up -d

# Optional: Set up Nginx reverse proxy
sudo cp nginx.conf /etc/nginx/sites-available/bana-tts
sudo ln -s /etc/nginx/sites-available/bana-tts /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

## Important Considerations

### Model Size & Memory
Your TTS models are quite large. Ensure your hosting platform has:
- **RAM:** At least 2GB (4GB recommended)
- **Storage:** At least 5GB for models and application
- **CPU:** 1-2 cores minimum

### Performance Optimization

1. **Cold Start Issues:** Some platforms (like Cloud Run) might have cold start delays
2. **Model Loading:** Consider implementing model caching/preloading
3. **Concurrent Requests:** Your current setup handles one request at a time

### Security

1. **Rate Limiting:** Nginx config includes basic rate limiting
2. **CORS:** Already configured in your Flask app
3. **HTTPS:** Use platform's built-in SSL or configure Let's Encrypt

### Costs Comparison

| Platform | Monthly Cost | Pros | Cons |
|----------|-------------|------|------|
| Railway | $5 | Easiest setup | Limited resources |
| DigitalOcean | $5-12 | Good balance | Manual scaling |
| Google Cloud Run | $0-10 | Pay-per-use | Cold starts |
| Heroku | $7 | Simple | Expensive for resources |
| VPS | $5-20 | Full control | Requires maintenance |

## Recommended Deployment Flow

1. **Test Locally First:**
   ```bash
   docker-compose up -d
   # Test at http://localhost:5000
   ```

2. **Choose Platform Based on Needs:**
   - **Learning/Testing:** Railway or DigitalOcean
   - **Production:** VPS or Google Cloud Run
   - **Scaling:** AWS ECS or Google Cloud Run

3. **Monitor and Optimize:**
   - Set up logging
   - Monitor memory/CPU usage
   - Implement health checks

## Getting Your App URL

After deployment, you'll get a public URL like:
- Railway: `https://bana-tts-production.up.railway.app`
- Heroku: `https://your-app-name.herokuapp.com`
- Google Cloud Run: `https://bana-tts-hash-uc.a.run.app`

## Need Help?

1. Check the deployment logs on your chosen platform
2. Ensure model files are properly included in the Docker image
3. Verify the Flask app runs on `0.0.0.0:5000` (already configured)
4. Test the `/speak` endpoint with a POST request

## Sample Frontend Integration

```javascript
// Test your deployed API
const response = await fetch('https://your-deployed-url.com/speak', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    text: 'Hello world', 
    gender: 'male' 
  })
});
const data = await response.json();
// data.speech contains base64 encoded audio
```
