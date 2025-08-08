# Quick Railway Deployment Guide

## Prerequisites
1. GitHub account
2. Railway account (free)
3. Your code pushed to GitHub

## Steps

### 1. Prepare Your Repository
```bash
# Make sure your code is on GitHub
git add .
git commit -m "Prepare for Railway deployment"
git push origin master
```

### 2. Deploy to Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `bana-tts` repository
6. Railway automatically detects your Dockerfile
7. Click "Deploy"

### 3. Configure Environment (if needed)
- Railway auto-detects port 5000 from your Dockerfile
- No additional configuration needed

### 4. Get Your URL
- Railway provides a URL like: `https://bana-tts-production.up.railway.app`
- Your app will be live immediately

## Expected Results
- ✅ Build time: 5-10 minutes (first time)
- ✅ Memory usage: ~2-3GB
- ✅ Your $5 free credit covers ~50-100 hours of usage
- ✅ Perfect for testing and demos

## Testing Your Deployment
Once deployed, test your endpoints:
```bash
# Test the web interface
curl https://your-app.railway.app/

# Test the API
curl -X POST https://your-app.railway.app/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","gender":"male"}'
```

## Notes
- Railway is perfect for Docker apps
- Free credits refresh monthly
- Automatic HTTPS included
- No server management required
