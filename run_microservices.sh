#!/bin/bash

# Ensure Podman machine is running
echo "🔍 Checking Podman machine status..."
if ! podman info > /dev/null 2>&1; then
    echo "⚠️ Podman machine is not running. Starting it now..."
    podman machine start
    if [ $? -ne 0 ]; then
        echo "❌ Failed to start Podman machine."
        exit 1
    fi
    echo "✅ Podman machine started."
else
    echo "✅ Podman is already running."
fi

# Function to stop and run containers
start_service() {
  name=$1
  port=$2
  path=$3

  echo "🔁 Restarting $name..."
  podman stop ${name}_container 2>/dev/null
  podman rm ${name}_container 2>/dev/null

  echo "🔧 Building $name..."
  podman build -t $name $path

  echo "🚀 Running $name on port $port..."
  podman run -d --name ${name}_container -p ${port}:${port} $name
}

start_service user_service 5001 ./user_service
start_service watch_history_service 5002 ./watch_history_service
start_service rating_service 5003 ./rating_service

echo "✅ All services are running:
- http://localhost:5001 (user_service)
- http://localhost:5002 (watch_history_service)
- http://localhost:5003 (rating_service)"
