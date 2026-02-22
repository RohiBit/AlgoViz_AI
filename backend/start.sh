#!/bin/bash
# Start the Celery worker in the background
celery -A celery_worker worker --loglevel=info &

# Start the FastAPI web server
uvicorn main:app --host 0.0.0.0 --port 8000