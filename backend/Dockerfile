# Backend Dockerfile - FastAPI with Manim, Celery, and Gemini  
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Manim rendering
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpango-1.0-0 \
    libpango-1.0-dev \
    libpangoft2-1.0-0 \
    fonts-dejavu \
    texlive \
    texlive-fonts-recommended \
    texlive-latex-extra \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
