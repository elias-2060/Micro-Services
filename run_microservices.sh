#!/bin/bash

# Check if Podman is installed and working
echo "🔍 Checking Podman..."
if ! command -v podman > /dev/null; then
    echo "❌ Podman is not installed. Please install Podman first."
    exit 1
fi

if ! podman info > /dev/null 2>&1; then
    echo "❌ Podman is not functioning correctly. Check permissions or installation."
    exit 1
fi

echo "✅ Podman is ready."

# Stop and remove existing containers
echo "🛑 Stopping and removing existing containers..."
podman-compose down

# Build and start services
echo "🚀 Starting services with Podman..."
podman-compose up -d --build

echo "✅ All services are running:
- http://user_service:5001 (user service)
- http://watch_history_service:5002 (watch history service)
- http://rating_service:5003 (rating service)
- http://recommendation_service:5004 (Recommendation Service)
- http://newsfeed_service:5005 (Newsfeed Service)
- http://movie_service:5006 (Movie Service)"

echo "🌐 Swagger UI available at  http://localhost:5000/apidocs/"