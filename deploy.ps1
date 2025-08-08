# Bana TTS Deployment Helper for Windows
# PowerShell script to help deploy your TTS application

Write-Host "🚀 Bana TTS Deployment Helper" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Download from: https://docs.docker.com/desktop/windows/" -ForegroundColor Yellow
    exit 1
}

# Check if docker-compose is available
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose is available: $composeVersion" -ForegroundColor Green
} catch {
    try {
        $composeVersion = docker compose version
        Write-Host "✅ Docker Compose is available: $composeVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker Compose is not available." -ForegroundColor Red
        exit 1
    }
}

# Build the Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build -t bana-tts:latest .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to build Docker image" -ForegroundColor Red
    exit 1
}

# Show deployment options
Write-Host ""
Write-Host "📋 Deployment Options:" -ForegroundColor Cyan
Write-Host "1. Local deployment (docker-compose)" -ForegroundColor White
Write-Host "2. Show cloud deployment instructions" -ForegroundColor White
Write-Host "3. Export Docker image for manual deployment" -ForegroundColor White

$choice = Read-Host "Choose an option (1-3)"

switch ($choice) {
    "1" {
        Write-Host "🐳 Starting local deployment with Docker Compose..." -ForegroundColor Yellow
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Application is running at http://localhost:5000" -ForegroundColor Green
            Write-Host "📊 To check logs: docker-compose logs -f" -ForegroundColor Yellow
            Write-Host "🛑 To stop: docker-compose down" -ForegroundColor Yellow
            
            # Try to open the URL in the default browser
            try {
                Start-Process "http://localhost:5000"
            } catch {
                Write-Host "Could not open browser automatically. Please visit http://localhost:5000" -ForegroundColor Yellow
            }
        } else {
            Write-Host "❌ Failed to start the application" -ForegroundColor Red
        }
    }
    
    "2" {
        Write-Host @"

☁️  CLOUD DEPLOYMENT OPTIONS:

1. **Railway (Easiest)** 🌟
   - Push your code to GitHub
   - Go to https://railway.app
   - Connect GitHub repo → Railway auto-deploys
   - Cost: $5/month starter plan

2. **DigitalOcean App Platform**
   - Push code to GitHub
   - Go to DigitalOcean App Platform
   - Connect repo and deploy
   - Cost: $5-12/month

3. **Heroku Container Registry**
   Commands to run:
   heroku login
   heroku container:login
   heroku create your-app-name
   heroku container:push web
   heroku container:release web

4. **Google Cloud Run**
   gcloud builds submit --tag gcr.io/PROJECT-ID/bana-tts
   gcloud run deploy --image gcr.io/PROJECT-ID/bana-tts

5. **VPS Deployment**
   - Rent a VPS (DigitalOcean, Linode, AWS EC2)
   - Copy docker-compose.yml to server
   - Run: docker-compose up -d
   - Cost: $5-20/month

📖 For detailed instructions, see DEPLOYMENT.md

"@ -ForegroundColor White
    }
    
    "3" {
        Write-Host "📦 Exporting Docker image..." -ForegroundColor Yellow
        
        # Use PowerShell pipeline instead of bash pipe
        docker save bana-tts:latest | gzip > bana-tts-docker-image.tar.gz
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker image exported to: bana-tts-docker-image.tar.gz" -ForegroundColor Green
            Write-Host "📤 Copy this file to your server and load it with:" -ForegroundColor Yellow
            Write-Host "   gunzip -c bana-tts-docker-image.tar.gz | docker load" -ForegroundColor White
            
            # Show file size
            $fileSize = (Get-Item "bana-tts-docker-image.tar.gz").Length / 1MB
            Write-Host "📏 File size: $($fileSize.ToString('F2')) MB" -ForegroundColor Cyan
        } else {
            Write-Host "❌ Failed to export Docker image" -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Done! Check DEPLOYMENT.md for more detailed instructions." -ForegroundColor Green
