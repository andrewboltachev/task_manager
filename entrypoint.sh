#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

export PATH=/app/.venv/bin/:$PATH

uv sync

# The DB is guaranteed to be ready here because of Docker 'service_healthy'

echo "Running migrations..."
python manage.py migrate

# Execute the main command (Gunicorn or runserver)
exec "$@"
