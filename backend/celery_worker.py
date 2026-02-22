from celery import Celery
import subprocess
import os

# Initialize Celery to use Redis (make sure Redis is running on your laptop!)
app = Celery('tasks', broker='redis://localhost:6379/0')

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
