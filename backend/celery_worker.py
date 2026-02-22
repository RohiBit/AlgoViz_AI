from celery import Celery
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Redis URL from environment (Upstash or local)
# Strip trailing slashes to prevent connection issues
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0").rstrip('/')

# Initialize Celery app
app = Celery('algoviz')

# Explicitly set broker and result backend URLs
app.conf.broker_url = REDIS_URL
app.conf.result_backend = REDIS_URL

# Configure SSL for rediss:// URLs
redis_ssl_config = {}
broker_use_ssl = REDIS_URL.startswith('rediss://')

if broker_use_ssl:
    redis_ssl_config = {
        'ssl_cert_reqs': 'CERT_REQUIRED',
        'ssl_ca_certs': None,  # Use system default CA bundle
        'ssl_certfile': None,
        'ssl_keyfile': None,
    }

# Celery configuration for Upstash Redis with SSL support
app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_pool_limit=None,  # Don't limit connection pool for Upstash
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # For Upstash SSL connections (rediss://)
    broker_use_ssl=broker_use_ssl,
    redis_backend_use_ssl=redis_ssl_config,
)

print(f"✅ Celery configured with Redis")
print(f"   Broker URL: {REDIS_URL}")
print(f"   Result Backend: {REDIS_URL}")
print(f"   SSL enabled: {broker_use_ssl}")
print(f"   URL stripped: {REDIS_URL == REDIS_URL.rstrip('/')}")

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
