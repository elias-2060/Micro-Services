#!/bin/bash

# Default frontend port
PORT=3000

# Kill process using the port, if any
PID=$(lsof -ti tcp:$PORT)
if [ -n "$PID" ]; then
  echo "Port $PORT is in use by PID $PID. Killing it..."
  kill -9 $PID || { echo "Failed to kill process $PID"; exit 1; }
  # Ensure the process is killed before continuing
  sleep 1
else
  echo "No process found using port $PORT."
fi

# Navigate to the frontend directory
cd frontend || { echo "frontend directory not found"; exit 1; }

# Install frontend dependencies
if [ -f "package.json" ]; then
  echo "Installing frontend dependencies..."
  npm install
else
  echo "package.json not found in frontend directory"
  exit 1
fi

# Run the frontend
echo "Starting frontend on port $PORT..."
npm start
