#! /usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# 1. Let the DB wake up
echo "Running Pre-Start Script..."
python backend_pre_start.py

# 2. Apply Database Migrations
echo "Running Alembic Migrations..."
alembic upgrade head

# 3. Create Initial Data (Admin User)
echo "Seeding Initial Data..."
python -m app.initial_data

# 4. Start the Server
echo "Starting Production Server..."
# Web Concurrency = Number of CPU cores * 2 + 1 (Standard Formula)
# We bind to 0.0.0.0 so Docker can map the port
exec gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000