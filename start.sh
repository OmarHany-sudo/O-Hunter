#!/bin/bash

# O-Hunter Startup Script for Railway
echo "Starting O-Hunter Web Vulnerability Scanner..."

# Set environment variables
export PYTHONPATH=/app
export PORT=${PORT:-8080}

# Navigate to the core directory
cd /app/core

# Start the Flask application
python app.py

