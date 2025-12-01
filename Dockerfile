# Use an official Python runtime as a parent image
FROM python:3.14-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_ENV=prod \
    # CRITICAL: Define the venv location explicitly
    VIRTUAL_ENV=/app/.venv \
    # Add venv to PATH so 'python' automatically calls the venv python
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
# uv will detect $VIRTUAL_ENV and install packages there.
RUN uv sync --frozen --no-dev --no-install-project --group prod

# Copy the rest of the application code
COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Install the project itself (if needed, or just rely on source copy)
# This step ensures that if your project is a package, it's installed.
# If not, you can skip this, but it's good practice.
RUN uv sync --frozen --no-dev --group prod

# Collect static files
# Now 'python' resolves to '/app/.venv/bin/python' which has Django
RUN SECRET_KEY=dummy python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app/.venv
USER appuser

# Expose port
EXPOSE 8000

# Set the Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_manager.wsgi:application"]
