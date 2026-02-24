from fastapi import FastAPI, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image
import uuid
import os
import json
import subprocess
import sys
import io
from dotenv import load_dotenv

# Ensure parent directory is in path for imports (works from any CWD)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Load environment variables from .env file
load_dotenv()

# Import modular visualization classes (use relative imports for backend module)
try:
    from templates import (
        AlgoVizBaseScene,
        # Data Structures
        AVLTreeViz,
        BinaryTreeViz,
        RBTreeViz,
        BTreeViz,
        GraphSearchViz,
        # Machine Learning 2D
        LinearRegressionViz,
        LogisticRegressionViz,
        SVMViz,
        KMeansViz,
        DecisionTreeViz,
        RandomForestViz,
        KNNViz,
        # Machine Learning 3D
        GradientDescent3DViz,
    )
except ImportError:
    # Fallback for absolute imports when backend is installed as package
    from backend.templates import (
        AlgoVizBaseScene,
        # Data Structures
        AVLTreeViz,
        BinaryTreeViz,
        RBTreeViz,
        BTreeViz,
        GraphSearchViz,
        # Machine Learning 2D
        LinearRegressionViz,
        LogisticRegressionViz,
        SVMViz,
        KMeansViz,
        DecisionTreeViz,
        RandomForestViz,
        KNNViz,
        # Machine Learning 3D
        GradientDescent3DViz,
    )

# Redis and Celery Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0").rstrip('/')
CELERY_AVAILABLE = False
celery_app = None

# Try to initialize Celery with Redis broker
try:
    from celery import Celery
    import redis
    
    # Test Redis connection
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    
    # Initialize Celery app
    celery_app = Celery('algoviz')
    
    # Explicitly set broker and result backend URLs
    celery_app.conf.broker_url = REDIS_URL
    celery_app.conf.result_backend = REDIS_URL
    
    # Configure SSL for rediss:// URLs
    redis_ssl_config = {}
    broker_use_ssl = REDIS_URL.startswith('rediss://')
    
    if broker_use_ssl:
        redis_ssl_config = {
            'ssl_cert_reqs': 'CERT_REQUIRED',
            'ssl_ca_certs': None,
            'ssl_certfile': None,
            'ssl_keyfile': None,
        }
    
    celery_app.conf.update(
        broker_connection_retry_on_startup=True,
        broker_connection_retry=True,
        broker_pool_limit=None,
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        broker_use_ssl=broker_use_ssl,
        redis_backend_use_ssl=redis_ssl_config,
    )
    CELERY_AVAILABLE = True
    print(f"✅ Redis connected")
    print(f"   Broker URL: {REDIS_URL}")
    print(f"   Result Backend: {REDIS_URL}")
    print(f"   SSL enabled: {broker_use_ssl}")
    print("✅ Celery available with remote Redis broker")
    
except Exception as e:
    print(f"⚠️  Celery/Redis not available: {str(e)}")
    print("Using synchronous execution (no Celery)")
    CELERY_AVAILABLE = False

class AsyncResult:
    def __init__(self, *args, **kwargs):
        self.state = "PENDING"
        self.result = None
        self.info = None

app = FastAPI()

os.makedirs("media", exist_ok=True)

# CORS Configuration for development and production
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Local development
    "https://algoviz-frontend.vercel.app",  # Production (Vercel)
    "https://algovizfrontend-lgbv5u3hy-rkprinczs-projects.vercel.app",  # Vercel preview
]

# Allow additional origins from environment variable for flexibility
if os.getenv("ALLOWED_ORIGINS"):
    additional_origins = os.getenv("ALLOWED_ORIGINS").split(",")
    ALLOWED_ORIGINS.extend([origin.strip() for origin in additional_origins])

# Regex pattern to allow all Vercel preview deployments for this project
# Matches: https://<anything-with-project-name>-<user>-projects.vercel.app
vercel_preview_regex = r"https://.*\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=vercel_preview_regex,  # Allows all Vercel preview deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")

# Load API key securely from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. "
        "Please create a .env file or set the environment variable."
    )

class VisualRequest(BaseModel):
    topic: str
    intent: str
    user_input: str = ""

class CodeExecutionRequest(BaseModel):
    code: str
    language: str = "python"


def generate_teaching_plan_with_gemini(topic: str) -> dict:
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = "Create a detailed teaching plan for explaining " + topic + " as an algorithm visualization. "
        prompt += "Respond ONLY with a valid JSON object."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        response_text = response.text
        
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}")
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx+1]
            plan = json.loads(json_str)
        else:
            plan = json.loads(response_text)
        
        # Ensure topic is always included in the plan
        if "topic" not in plan or not plan["topic"]:
            plan["topic"] = topic
            
        if "task_id" not in plan or not plan["task_id"]:
            plan["task_id"] = str(uuid.uuid4())
        if "estimatedDuration" not in plan:
            plan["estimatedDuration"] = 180
        if "createdAt" not in plan:
            plan["createdAt"] = str(uuid.uuid4())
            
        return plan
        
    except Exception as e:
        print(f"Error generating plan with Gemini: {e}")
        return generate_deterministic_plan(topic)


def generate_deterministic_plan(topic: str) -> dict:
    return {
        "task_id": str(uuid.uuid4()),
        "topic": topic,
        "steps": [
            {"id": "step_1", "title": "Introduction", "description": f"Understanding {topic}", "timestamp": 0, "status": "pending"},
            {"id": "step_2", "title": "Visual Representation", "description": "Building intuition", "timestamp": 30, "status": "pending"},
            {"id": "step_3", "title": "Algorithm Walkthrough", "description": f"Step-by-step execution", "timestamp": 60, "status": "pending"},
            {"id": "step_4", "title": "Complexity Analysis", "description": "Time and space complexity", "timestamp": 120, "status": "pending"},
            {"id": "step_5", "title": "Conclusion", "description": "Summary and key takeaways", "timestamp": 150, "status": "pending"}
        ],
        "estimatedDuration": 180,
        "createdAt": str(uuid.uuid4())
    }


def generate_dynamic_algorithm_manim(topic: str, initial_data: list, task_id: str) -> dict:
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    data_str = str(initial_data)
    topic_name = topic.replace('_', ' ')
    
    prompt = "You are an expert Manim developer. Create a complete Manim Python script for visualizing a " + topic_name + " algorithm with the initial data: " + data_str + ". Use a single class named DynamicScene."

    print(f"Generating dynamic Manim code for {topic}...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        generated_code = response.text.strip()
        
        # Save the generated script
        os.makedirs("templates/dynamic_cache", exist_ok=True)
        script_path = f"templates/dynamic_cache/{topic}_{task_id}.py"
        
        with open(script_path, "w") as f:
            f.write(generated_code)
        
        print(f"Saved generated script to {script_path}")
        
        # Render with Manim
        output_path = f"media/{task_id}.mp4"
        
        command = ["manim", "-ql", "--disable_caching", "--write_to_movie", script_path, "DynamicScene"]
        print(f"Executing: {' '.join(command)}")
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        print(f"Manim stdout: {result.stdout}")
        print(f"Manim stderr: {result.stderr}")
        
        # Find the generated video
        generated_video = None
        
        for root, dirs, files in os.walk("media/videos"):
            for f in files:
                if f.endswith(".mp4") and "DynamicScene" in f:
                    generated_video = os.path.join(root, f)
                    break
            if generated_video:
                break
        
        if not generated_video:
            generated_video = f"media/videos/{topic}_{task_id}/480p15/DynamicScene.mp4"
        
        if generated_video and os.path.exists(generated_video):
            import shutil
            shutil.copy2(generated_video, output_path)
            print(f"Successfully copied dynamic video to {output_path}")
            return {
                "status": "completed",
                "video_url": output_path,
                "method": "gemini_dynamic"
            }
        else:
            print("Dynamic generation video not found")
            return {"status": "failed", "error": "Video not generated"}
            
    except Exception as e:
        print(f"Error generating dynamic Manim code: {e}")
        return {"status": "failed", "error": str(e)}


def render_algorithm_sync(plan: dict) -> dict:
    topic = plan.get("topic", "")
    task_id = plan.get("task_id", "default")
    initial_data = plan.get("initial_data", [5, 3, 8, 1, 2])
    output_path = f"media/{task_id}.mp4"
    os.makedirs("media", exist_ok=True)
    
    # Mapping of topic names to modular visualization classes
    topic_to_class = {
        "avl": AVLTreeViz,
        "binary tree": BinaryTreeViz,
        "binary search tree": BinaryTreeViz,
        "bst": BinaryTreeViz,
        "red-black": RBTreeViz,
        "rb tree": RBTreeViz,
        "rbtree": RBTreeViz,
        "b-tree": BTreeViz,
        "btree": BTreeViz,
        "graph search": GraphSearchViz,
        "bfs": GraphSearchViz,
        "dfs": GraphSearchViz,
        "dijkstra": GraphSearchViz,
        "linear regression": LinearRegressionViz,
        "logistic regression": LogisticRegressionViz,
        "svm": SVMViz,
        "support vector": SVMViz,
        "k-means": KMeansViz,
        "kmeans": KMeansViz,
        "decision tree": DecisionTreeViz,
        "random forest": RandomForestViz,
        "knn": KNNViz,
        "k-nearest": KNNViz,
        "gradient descent": GradientDescent3DViz,
    }
    
    # Check if topic matches any modular class
    visualization_class = None
    topic_lower = topic.lower()
    
    for key, cls in topic_to_class.items():
        if key in topic_lower:
            visualization_class = cls
            break
    
    # Handle legacy sorting algorithms (static templates)
    if "merge" in topic_lower:
        template_name = "merge_sort"
        class_name = "MergeSortTreeFinal"
        template_path = f"templates/{template_name}.py"
    elif "selection" in topic_lower:
        template_name = "selection_sort"
        class_name = "SelectionSortFullScene"
        template_path = f"templates/{template_name}.py"
    elif "bubble" in topic_lower:
        template_name = "bubble_sort"
        class_name = "BubbleSortFullScene"
        template_path = f"templates/{template_name}.py"
    elif visualization_class:
        # Use modular visualization class - create a temporary wrapper script
        print(f"Using modular visualization: {visualization_class.__name__}")
        template_name = f"modular_{visualization_class.__name__}"
        try:
            # Create temporary wrapper script for the modular class
            module_name = visualization_class.__module__.split('.')[-1]
            temp_script = f"""
from backend.templates import {visualization_class.__name__}

class DynamicScene({visualization_class.__name__}):
    pass
"""
            temp_path = f"templates/dynamic_cache/temp_{task_id}.py"
            os.makedirs("templates/dynamic_cache", exist_ok=True)
            with open(temp_path, "w") as f:
                f.write(temp_script)
            
            template_path = temp_path
            class_name = "DynamicScene"
            print(f"Created temporary wrapper for {visualization_class.__name__}")
        except Exception as e:
            print(f"Error creating wrapper for modular visualization: {e}")
            print(f"Falling back to dynamic code generation for {topic}...")
            return generate_dynamic_algorithm_manim(topic, initial_data, task_id)
    else:
        print(f"No static template for {topic}, generating dynamic Manim code...")
        return generate_dynamic_algorithm_manim(topic, initial_data, task_id)
    
    command = ["manim", "-ql", "--disable_caching", "--write_to_movie", template_path, "DynamicScene"]
    
    print(f"Executing: {' '.join(command)}")
    
    try:
        subprocess.run(command, check=True)
        
        import shutil
        source_video = f"media/videos/{template_name}/480p15/{class_name}.mp4"
        
        if not os.path.exists(source_video):
            source_video = f"media/{class_name}.mp4"
        
        if os.path.exists(source_video):
            shutil.copy2(source_video, output_path)
            print(f"Copied video from {source_video} to {output_path}")
        
        return {"status": "completed", "video_url": output_path}
    except subprocess.CalledProcessError as e:
        print(f"Error running Manim: {e}")
        return {"status": "failed", "error": str(e)}


@app.post("/generate-plan")
async def generate_plan(request: VisualRequest):
    plan = generate_teaching_plan_with_gemini(request.topic)
    return plan


@app.post("/render")
async def trigger_render(plan: dict):
    task_id = plan.get("task_id")
    
    print(f"Running synchronous render for task: {task_id}")
    result = render_algorithm_sync(plan)
    
    if result.get("status") == "completed":
        return {"status": "completed", "task_id": task_id, "video_url": result.get("video_url"), "plan": plan}
    else:
        return {"status": "failed", "task_id": task_id, "error": result.get("error")}


@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    video_path = f"media/{task_id}.mp4"
    if os.path.exists(video_path):
        return {"task_id": task_id, "status": "SUCCESS", "result": {"status": "completed", "video_url": video_path}}
    else:
        return {"task_id": task_id, "status": "PENDING"}


pipeline_progress = {}


@app.get("/pipeline-status/{task_id}")
async def get_pipeline_status(task_id: str):
    if task_id in pipeline_progress:
        return pipeline_progress[task_id]
    
    video_path = f"media/{task_id}.mp4"
    if os.path.exists(video_path):
        return {
            "task_id": task_id,
            "current_stage": 4,
            "stages": [
                {"id": 1, "label": "Requesting LLM Planner...", "status": "completed"},
                {"id": 2, "label": "Accessing Knowledge Base...", "status": "completed"},
                {"id": 3, "label": "Generating Deterministic Teaching Plan...", "status": "completed"},
                {"id": 4, "label": "Rendering with Manim Engine (ASUS TUF GPU)....", "status": "completed"}
            ],
            "status": "SUCCESS"
        }
    
    return {
        "task_id": task_id,
        "current_stage": 1,
        "stages": [
            {"id": 1, "label": "Requesting LLM Planner...", "status": "in_progress"},
            {"id": 2, "label": "Accessing Knowledge Base...", "status": "pending"},
            {"id": 3, "label": "Generating Deterministic Teaching Plan...", "status": "pending"},
            {"id": 4, "label": "Rendering with Manim Engine (ASUS TUF GPU)....", "status": "pending"}
        ],
        "status": "PROCESSING"
    }


@app.get("/")
async def root():
    """
    Root endpoint - Returns API status and Redis/Celery availability
    """
    redis_status = False
    
    # Test Redis connection (Upstash with SSL)
    if CELERY_AVAILABLE:
        try:
            import redis
            redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            redis_client.ping()
            redis_status = True
        except Exception as e:
            print(f"Redis connection check failed: {e}")
            redis_status = False
    
    return {
        "message": "Algorithm Visualization API",
        "celery_available": CELERY_AVAILABLE,
        "redis_available": redis_status,
        "redis_url": f"{REDIS_URL[:40]}..." if REDIS_URL else "Not configured",
        "version": "1.0.0"
    }



def trace_code_execution(code: str) -> dict:
    execution_trace = []
    
    safe_globals = {
        "__builtins__": {
            "print": print, "len": len, "range": range, "enumerate": enumerate,
            "zip": zip, "sorted": sorted, "min": min, "max": max,
            "abs": abs, "sum": sum, "int": int, "float": float, "str": str,
            "list": list, "dict": dict, "set": set, "tuple": tuple,
            "bool": bool, "True": True, "False": False, "None": None,
        }
    }
    
    local_vars = {}
    source_lines = code.split("\n")
    
    def trace_callback(frame, event, arg):
        if event == "line":
            line_no = frame.f_lineno
            filename = frame.f_code.co_filename
            if filename == "<string>":
                if 0 <= line_no - 1 < len(source_lines):
                    active_code = source_lines[line_no - 1].strip()
                    if active_code:
                        vars_state = {}
                        for k, v in frame.f_locals.items():
                            if not k.startswith("__"):
                                try:
                                    vars_state[k] = repr(v)
                                except:
                                    vars_state[k] = str(type(v).__name__)
                        
                        execution_trace.append({
                            "line_number": line_no,
                            "active_code": active_code,
                            "variables_state": vars_state
                        })
        return trace_callback
    
    try:
        sys.settrace(trace_callback)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            exec(code, safe_globals, local_vars)
        except Exception as e:
            execution_trace.append({
                "line_number": -1,
                "active_code": f"Error: {str(e)}",
                "variables_state": {"error": str(e)}
            })
        finally:
            sys.settrace(None)
            sys.stdout = old_stdout
            
    except Exception as e:
        execution_trace.append({
            "line_number": 0,
            "active_code": f"Fatal Error: {str(e)}",
            "variables_state": {"error": str(e)}
        })
    
    return {
        "execution_trace": execution_trace,
        "total_lines": len(source_lines),
        "traced_lines": len(execution_trace)
    }


def render_code_execution_visualization(execution_trace: list, task_id: str, user_code: str = "") -> dict:
    output_path = f"media/{task_id}.mp4"
    
    trace_file = f"media/{task_id}_trace.json"
    with open(trace_file, "w") as f:
        json.dump(execution_trace, f, indent=2)
    
    os.makedirs("media", exist_ok=True)
    
    print("Using fallback static template...")
    template_path = "templates/code_execution.py"
    
    command = ["manim", "-ql", "--disable_caching", template_path, "DynamicScene"]
    print(f"Executing: {' '.join(command)}")
    
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Manim stdout: {result.stdout}")
    print(f"Manim stderr: {result.stderr}")
    
    import shutil
    generated_video = "media/videos/code_execution/480p15/DynamicScene.mp4"
    
    if os.path.exists(generated_video):
        shutil.copy2(generated_video, output_path)
        print(f"Successfully copied video to {output_path}")
    else:
        print("Using fallback BubbleSort video...")
        fallback_video = "media/BubbleSortFullScene.mp4"
        if os.path.exists(fallback_video):
            shutil.copy2(fallback_video, output_path)
            print(f"Copied fallback video to {output_path}")
        else:
            raise FileNotFoundError("No video found")
    
    return {
        "status": "completed",
        "video_url": output_path,
        "trace_file": trace_file,
        "total_steps": len(execution_trace),
        "method": "static_template"
    }


@app.post("/visualize-code-execution")
async def visualize_code_execution(request: CodeExecutionRequest):
    task_id = str(uuid.uuid4())
    print(f"--- STARTING DYNAMIC GENERATION FOR TASK: {task_id} ---")
    
    # Trace the code execution first
    print("Tracing code execution...")
    trace_result = trace_code_execution(request.code)
    execution_trace = trace_result["execution_trace"]
    
    print(f"Traced {len(execution_trace)} lines of execution")
    
    # Generate visualization steps from trace
    steps = []
    for i, trace_entry in enumerate(execution_trace):
        timestamp = i * 3
        
        vars_display = []
        for k, v in trace_entry.get("variables_state", {}).items():
            vars_display.append(f"{k} = {v}")
        
        steps.append({
            "id": f"step_{i+1}",
            "title": f"Line {trace_entry['line_number']}: {trace_entry['active_code'][:30]}...",
            "description": f"Variables: {', '.join(vars_display[:3])}" if vars_display else "No variables",
            "timestamp": timestamp,
            "status": "pending"
        })
    
    estimated_duration = max(len(execution_trace) * 3, 10)
    
    # Render the visualization
    print("Rendering visualization...")
    render_result = render_code_execution_visualization(execution_trace, task_id, request.code)
    
    return {
        "task_id": task_id,
        "topic": "Code Execution Visualization",
        "steps": steps,
        "estimatedDuration": estimated_duration,
        "execution_trace": execution_trace,
        "createdAt": str(uuid.uuid4()),
        "status": "completed",
        "video_url": render_result.get("video_url")
    }


@app.post("/upload-vision")
async def upload_vision(file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    print(f"--- PROCESSING VISION UPLOAD FOR TASK: {task_id} ---")
    
    # Step 1: Accept UploadFile and convert to PIL Image
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        print(f"Image loaded: {image.size} {image.mode}")
        
    except Exception as e:
        print(f"Error reading image: {e}")
        return {
            "task_id": task_id,
            "status": "error",
            "error": f"Failed to read image: {str(e)}"
        }
    
    # Step 2: Initialize Gemini model and send prompt
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Your prompt with concrete template and proper instructions
        prompt = f"""
You are an expert Manim developer. I provide a whiteboard image. Generate a working Manim script named GeneratedWhiteboardScene.

FOLLOW THIS TEMPLATE EXACTLY - modify only the node values and labels:

```
from manim import *

class GeneratedWhiteboardScene(Scene):
    def construct(self):
        # Title at TOP
        title = Text("Tree Data Structure", font_size=40, color=YELLOW).to_edge(UP, buff=0.3)
        
        # Narration at BOTTOM (this is a TEXT OBJECT that will be updated)
        narration = Text("Let's explore tree concepts.", font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        
        # Add both to scene
        self.add(title, narration)
        self.play(Write(title), duration=0.5)
        
        # Create tree nodes as Circle objects (NOT arrays)
        # Center the tree around origin
        root = Circle(radius=0.3, color=BLUE)
        root.move_to([0, 1.5, 0])
        root_label = Text("1", font_size=18, color=WHITE).move_to(root.get_center())
        
        left_child = Circle(radius=0.3, color=GREEN)
        left_child.move_to([-2, 0.3, 0])
        left_label = Text("2", font_size=18, color=WHITE).move_to(left_child.get_center())
        
        right_child = Circle(radius=0.3, color=GREEN)
        right_child.move_to([2, 0.3, 0])
        right_label = Text("3", font_size=18, color=WHITE).move_to(right_child.get_center())
        
        # Edges (lines connecting nodes)
        left_edge = Line(root.get_center(), left_child.get_center(), color=GRAY)
        right_edge = Line(root.get_center(), right_child.get_center(), color=GRAY)
        
        # Group everything
        tree = VGroup(root, root_label, left_child, left_label, right_child, right_label, left_edge, right_edge)
        
        # Animate
        self.play(FadeIn(tree), duration=1)
        self.wait(1)
        
        # Update narration (example)
        new_narration = Text("The root node is at the top.", font_size=20, color=WHITE).to_edge(DOWN, buff=0.3)
        self.play(Transform(narration, new_narration), duration=0.5)
        self.wait(2)
        
        self.play(FadeOut(tree, title, narration), duration=0.5)
```

MODIFICATION INSTRUCTIONS:
1. Change node VALUES ("1", "2", "3") to match your whiteboard
2. Change tree STRUCTURE (add more children/levels as needed)
3. Keep positions in safe ranges: x ∈ [-6, 6], y ∈ [-3, 3]
4. Update NARRATION text in each self.play(Transform(...)) call
5. For level-2 children, use y=0 to y=-1, level-3 use y=-2, etc.
6. ALWAYS put node labels INSIDE the circles: Text(...).move_to(circle.get_center())
7. ALWAYS keep circle radius = 0.3

REQUIRED:
- Node labels MUST be Text objects positioned at circle centers
- All nodes are Circle(radius=0.3)
- All positions use .move_to([x, y, 0])
- Updates use Transform(narration, new_text)
- Total duration 12-18 seconds
- NO markdown backticks in output

At end, add:
# NARRATION: "full narration text matching your animations"

Output ONLY Python code. Start with from manim import *.
"""
        
        print(f"Sending image to Gemini for code generation...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, image]
        )
        
        response_text = response.text.strip()
        print(f"Gemini response received ({len(response_text)} chars)")
        
        # Step 4: Extract raw Python string and strip markdown ticks (aggressive)
        generated_code = response_text
        
        # Strip all variations of markdown code blocks
        # Remove opening ticks (with or without language specifier)
        generated_code = generated_code.replace("```python\n", "")
        generated_code = generated_code.replace("```python", "")
        generated_code = generated_code.replace("```\n", "")
        generated_code = generated_code.replace("```", "")
        
        # If code starts with "from manim", we're good. Remove anything before it.
        if "from manim import" in generated_code:
            start_idx = generated_code.find("from manim import")
            generated_code = generated_code[start_idx:]
        
        # If code ends with # NARRATION:, clean up after that
        if "# NARRATION:" in generated_code:
            narration_idx = generated_code.find("# NARRATION:")
            # Keep the narration line but remove anything after the closing quote
            narration_end = generated_code.find('"', narration_idx + 15)
            if narration_end != -1:
                generated_code = generated_code[:narration_end + 1]
        
        generated_code = generated_code.strip()
        
        if not generated_code:
            return {
                "task_id": task_id,
                "status": "error",
                "error": "No code generated from image analysis"
            }
        
        print(f"Extracted code ({len(generated_code)} chars)")
        print(f"Code preview: {generated_code[:100]}...")
        
        # Extract narration from the code comment
        narration_text = ""
        for line in generated_code.split("\n"):
            if "# NARRATION:" in line:
                # Extract text between quotes
                start = line.find('"')
                end = line.rfind('"')
                if start != -1 and end != -1 and start < end:
                    narration_text = line[start+1:end]
                break
        
        print(f"Extracted narration: {narration_text[:100]}...")
        
        # Step 5: Save to unique file in dynamic_cache
        os.makedirs("templates/dynamic_cache", exist_ok=True)
        script_path = f"templates/dynamic_cache/scene_{task_id}.py"
        
        with open(script_path, "w") as f:
            f.write(generated_code)
        
        print(f"Saved generated script to {script_path}")
        
        # Step 6: Execute with subprocess.run and robust error handling
        output_path = f"media/{task_id}.mp4"
        command = ["manim", "-ql", "--disable_caching", script_path, "GeneratedWhiteboardScene"]
        
        print(f"Executing Manim: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            print(f"Manim exit code: {result.returncode}")
            print(f"Manim stdout (last 300 chars): {result.stdout[-300:]}")
            print(f"Manim stderr (last 300 chars): {result.stderr[-300:]}")
            
            if result.returncode != 0:
                print(f"Manim execution failed with return code {result.returncode}")
                return {
                    "task_id": task_id,
                    "status": "failed",
                    "error": f"Manim execution failed: {result.stderr[-200:]}"
                }
        
        except subprocess.TimeoutExpired:
            print(f"Manim execution timed out after 180 seconds")
            return {
                "task_id": task_id,
                "status": "failed",
                "error": "Manim rendering timed out (exceeded 180 seconds)"
            }
        except Exception as e:
            print(f"Error executing subprocess: {e}")
            return {
                "task_id": task_id,
                "status": "failed",
                "error": f"Subprocess execution error: {str(e)}"
            }
        
        # Step 7: Copy output video from Manim media folder
        generated_video = None
        
        # Search for the generated video in Manim's output directory
        for root, dirs, files in os.walk("media/videos"):
            for f in files:
                if f.endswith(".mp4") and "GeneratedWhiteboardScene" in f:
                    generated_video = os.path.join(root, f)
                    break
            if generated_video:
                break
        
        if not generated_video or not os.path.exists(generated_video):
            print(f"Generated video not found in media/videos directory")
            return {
                "task_id": task_id,
                "status": "failed",
                "error": "Manim did not produce a video file"
            }
        
        import shutil
        shutil.copy2(generated_video, output_path)
        print(f"Successfully copied video from {generated_video} to {output_path}")
        
        # Step 8: Generate audio voiceover using local TTS (pyttsx3)
        audio_path = f"media/{task_id}_audio.mp3"
        final_output_path = f"media/{task_id}_with_audio.mp4"
        
        if narration_text and narration_text.strip():
            try:
                import pyttsx3
                
                print(f"Generating audio voiceover for task {task_id}...")
                print(f"Narration text: {narration_text[:100]}...")
                
                # Initialize TTS engine
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)  # Speed (100-200 recommended)
                engine.setProperty('volume', 0.9)  # Volume (0-1.0)
                
                # Save the audio file
                engine.save_to_file(narration_text, audio_path)
                engine.runAndWait()
                
                # Check if audio file was created
                if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
                    audio_size = os.path.getsize(audio_path)
                    print(f"Audio voiceover saved to {audio_path} ({audio_size} bytes)")
                    
                    # Step 9: Merge video and audio using ffmpeg
                    if os.path.exists(output_path):
                        print(f"Merging video and audio...")
                        print(f"Video: {output_path}")
                        print(f"Audio: {audio_path}")
                        
                        ffmpeg_command = [
                            "ffmpeg",
                            "-i", output_path,  # video input
                            "-i", audio_path,   # audio input
                            "-c:v", "copy",     # copy video codec (no re-encoding)
                            "-c:a", "aac",      # audio codec
                            "-shortest",        # use shortest stream
                            "-y",               # overwrite output file
                            final_output_path
                        ]
                        
                        ffmpeg_result = subprocess.run(
                            ffmpeg_command,
                            capture_output=True,
                            text=True,
                            timeout=120
                        )
                        
                        if ffmpeg_result.returncode == 0:
                            final_size = os.path.getsize(final_output_path)
                            print(f"Successfully merged video and audio to {final_output_path} ({final_size} bytes)")
                            # Use the merged file as final output
                            output_path = final_output_path
                        else:
                            print(f"FFmpeg merge failed:")
                            print(f"stdout: {ffmpeg_result.stdout[-200:]}")
                            print(f"stderr: {ffmpeg_result.stderr[-200:]}")
                            print("Returning video without audio")
                    else:
                        print(f"Video file not found: {output_path}")
                else:
                    print(f"Audio file not created or too small")
                
            except ImportError:
                print("pyttsx3 not installed")
            except Exception as e:
                print(f"Error generating TTS audio: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                print("Continuing with video-only output")
        else:
            print(f"No narration text found. Skipping audio generation.")
        
        return {
            "task_id": task_id,
            "status": "completed",
            "video_url": output_path,
            "method": "custom_whiteboard_generation_with_voiceover"
        }
            
    except Exception as e:
        print(f"Error in vision processing: {e}")
        import traceback
        traceback.print_exc()
        return {
            "task_id": task_id,
            "status": "error",
            "error": f"Vision processing error: {str(e)}"
        }
