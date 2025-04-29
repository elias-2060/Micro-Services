#!/bin/bash

# Ensure Podman machine is running
echo "Checking Podman machine status..."
if ! podman info > /dev/null 2>&1; then
    echo "Podman machine is not running. Attempting to start..."
    podman machine start
    if [ $? -ne 0 ]; then
        echo "❌ Failed to start Podman machine. Please check your installation."
        exit 1
    fi
    echo "✅ Podman machine started successfully."
else
    echo "✅ Podman is already running."
fi

# Stop and remove any existing containers
podman stop user_service_container 2>/dev/null
podman rm user_service_container 2>/dev/null
podman stop watch_history_service_container 2>/dev/null
podman rm watch_history_service_container 2>/dev/null

# Build the user_service container
echo "🔧 Building user_service..."
podman build -t user_service ./user_service

# Build the watch_history_service container
echo "🔧 Building watch_history_service..."
podman build -t watch_history_service ./watch_history_service

# Run the user_service container
echo "🚀 Running user_service on port 5001..."
podman run -d \
  --name user_service_container \
  -p 5001:5001 \
  user_service

# Run the watchhistory_service container
echo "🚀 Running watchhistory_service on port 5002..."
podman run -d \
  --name watch_history_service_container \
  -p 5002:5002 \
  watch_history_service

echo "✅ User Service is up and running at http://localhost:5001"
echo "✅ Watch History Service is up and running at http://localhost:5002"
