#!/bin/bash

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
npm start
