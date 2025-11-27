#!/bin/bash
# Database migration script for Kubernetes deployment
# This script should be run before starting the application

set -e

echo "🔄 Applying database migrations..."

# Set Flask app
export FLASK_APP=run.py

# Run migrations
flask db upgrade

echo "✓ Migrations applied successfully!"
