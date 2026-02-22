from celery import Celery
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Redis URL from environment (Upstash or local)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery app with Redis broker (supports rediss:// for SSL)
app = Celery(
    'algoviz',
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Celery configuration for Upstash Redis
app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_pool_limit=None,  # Don't limit connection pool for Upstash
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # For Upstash SSL connections
    broker_use_ssl=REDIS_URL.startswith('rediss://'),
    redis_backend_use_ssl={'ssl_certfile': None, 'ssl_keyfile': None} if REDIS_URL.startswith('rediss://') else {},
)

print(f"✅ Celery configured with Redis: {REDIS_URL[:40]}...")
print(f"✅ SSL enabled: {REDIS_URL.startswith('rediss://')}")

@app.task(name="render_algorithm")
def render_algorithm(plan):
    topic = plan.get("topic", "")
    task_id = plan.get("task_id", "default")
    
    # Determine which template to use based on the topic
    # Default to bubble_sort if no match
    template_name = "bubble_sort"
    if "merge" in topic.lower():
        template_name = "merge_sort"
    elif "selection" in topic.lower():
        template_name = "selection_sort"
    elif "bubble" in topic.lower():
        template_name = "bubble_sort"
    
    template_path = f"templates/{template_name}.py"
    output_path = f"media/{task_id}.mp4"
    
    # Create media directory if it doesn't exist
    os.makedirs("media", exist_ok=True)
    
    # The Deterministic Execution: Run Manim as a subprocess
    command = [
        "manim", "-pql", 
        "--disable_caching", 
        "--write_to_movie",
        template_path, 
        "DynamicScene"
    ]
    
    print(f"Executing: {' '.join(command)}")
    print(f"Output path: {output_path}")
    
    try:
        subprocess.run(command, check=True)
        return {"status": "completed", "video_url": output_path}
    except subprocess.CalledProcessError as e:
        print(f"Error running Manim: {e}")
        return {"status": "failed", "error": str(e)}
