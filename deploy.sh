#!/bin/bash

# Deployment script for Bana TTS Application
# This script helps deploy your TTS application to various hosting platforms

set -e

echo "🚀 Bana TTS Deployment Helper"
echo "=============================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t bana-tts:latest .

echo "✅ Docker image built successfully"

# Option 1: Local deployment
echo ""
echo "📋 Deployment Options:"
echo "1. Local deployment (docker-compose)"
echo "2. Show cloud deployment instructions"
echo "3. Export Docker image for manual deployment"

read -p "Choose an option (1-3): " choice

case $choice in
    1)
        echo "🐳 Starting local deployment with Docker Compose..."
        docker-compose up -d
        echo "✅ Application is running at http://localhost:5000"
        echo "📊 To check logs: docker-compose logs -f"
        echo "🛑 To stop: docker-compose down"
        ;;
    2)
        cat << 'EOF'

☁️  CLOUD DEPLOYMENT OPTIONS:

1. **DigitalOcean App Platform**
   - Push your code to GitHub
   - Connect GitHub repo to DigitalOcean App Platform
   - It will auto-detect Dockerfile and deploy
   - Cost: ~$5-12/month

2. **Heroku (with Container Registry)**
   ```bash
   heroku login
   heroku container:login
   heroku create your-app-name
   heroku container:push web
   heroku container:release web
   ```

3. **Google Cloud Run**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/bana-tts
   gcloud run deploy --image gcr.io/PROJECT-ID/bana-tts --platform managed
   ```

4. **AWS ECS/Fargate**
   - Push image to ECR
   - Create ECS service with Fargate
   - Set up load balancer

5. **Railway**
   - Connect GitHub repo
   - Railway auto-detects Dockerfile
   - Simple deployment with $5/month starter plan

6. **VPS (Ubuntu/CentOS)**
   - Copy docker-compose.yml to server
   - Run: docker-compose up -d
   - Set up nginx reverse proxy (nginx.conf provided)
   - Cost: $5-20/month depending on specs

EOF
        ;;
    3)
        echo "📦 Exporting Docker image..."
        docker save bana-tts:latest | gzip > bana-tts-docker-image.tar.gz
        echo "✅ Docker image exported to: bana-tts-docker-image.tar.gz"
        echo "📤 You can now copy this file to your server and load it with:"
        echo "   gunzip -c bana-tts-docker-image.tar.gz | docker load"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac
