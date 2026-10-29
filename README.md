# AlgoViz AI

An interactive learning platform designed to make algorithms easier to understand through visual animations and step-by-step explanations.

## Overview

Understanding algorithms from source code alone can be difficult. AlgoViz AI aims to make algorithm behavior more intuitive by presenting algorithm operations as visual animations.

The project separates its frontend and backend, providing a foundation for interactive algorithm learning and server-side visualization processing.

## Features

- Interactive algorithm visualization.
- Sorting algorithm demonstrations, including Bubble Sort, Merge Sort, and Selection Sort.
- Visual explanations of algorithm behavior.
- AI-assisted commentary and explanations.
- Backend processing for visualization tasks.
- Separate frontend and backend architecture.

## Technology Stack

- React
- TypeScript
- Python
- FastAPI
- Celery
- Redis and Manim, where configured in the backend deployment

## Architecture

- **Frontend:** Provides the user interface for selecting and exploring algorithms.
- **Backend:** Exposes API functionality through FastAPI.
- **Task processing:** Celery workers support background visualization jobs.
- **Rendering:** The visualization pipeline uses the configured animation-rendering dependencies.

The exact services and configuration required depend on the current deployment and backend implementation.

## Repository Structure

```text
AlgoViz_AI/
├── backend/
├── frontend/
├── docker-compose.yml
├── DEPLOYMENT.md
├── PRODUCTION_SETUP.md
└── README.md
```

## Getting Started

### Prerequisites

- Python
- Node.js and npm
- Redis, if required by the configured Celery worker
- The rendering dependencies required by the backend

### 1. Clone the repository

```bash
git clone https://github.com/RohiBit/AlgoViz_AI.git
cd AlgoViz_AI
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the backend using the entry point and configuration documented in the backend directory.

### 3. Set up the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by the development server.

### 4. Configure background processing

If your selected visualization workflow uses Celery and Redis, configure the broker and start the Redis service and Celery worker according to `REDIS_CELERY_SETUP.md` and the backend configuration.

## Learning Goals

This project explores the connection between algorithm design, visualization, frontend development, API design, and background task processing.

## Current Status

This README describes the documented architecture and features. Verify the complete startup sequence, external services, AI configuration, and deployed functionality before treating the project as production-ready.

## License

See the repository's `LICENSE` file for the applicable terms.
