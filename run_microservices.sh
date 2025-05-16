#!/bin/bash

VENV_DIR=".venv"

# Check if Podman is installed and working
echo "🔍 Checking Podman..."
if ! command -v podman > /dev/null; then
    echo "❌ Podman is not installed. Please install Podman first."
    exit 1
fi

if ! podman info > /dev/null 2>&1; then
    echo "❌ Podman is not running or functioning correctly. Check permissions or installation."
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
- http://localhost:5001 (User Service)
- http://localhost:5002 (Watch History Service)
- http://localhost:5003 (Rating Service)
- http://localhost:5004 (Recommendation Service)
- http://localhost:5005 (Newsfeed Service)
- http://localhost:5006 (Movie Service)

🌐 Swagger UI available for each microservice at their respective URLs /apidocs"
