# Backend Dockerfile - FastAPI with Manim, Celery, and Gemini  
FROM python:3.11-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies for Manim rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpango1.0-dev \
    fonts-dejavu \
    texlive \
    texlive-fonts-recommended \
    texlive-latex-extra \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Give start.sh execution permissions
RUN chmod +x /app/start.sh

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the start script (starts both Celery worker and FastAPI app)
CMD ["/app/start.sh"]
