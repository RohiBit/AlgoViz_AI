# Redis & Celery Configuration Guide - AlgoViz AI

## Overview

Your **AlgoViz AI** backend now supports distributed task processing using **Celery** with **Upstash Redis** as the message broker.

### What Changed

| Component | Before | After |
|-----------|--------|-------|
| **Redis Broker** | `redis://localhost:6379/0` (local) | `rediss://...@upstash.io:6379` (remote with SSL) |
| **Configuration** | Hardcoded URL | `REDIS_URL` environment variable |
| **SSL Support** | No | Yes (Upstash rediss://) |
| **Status Check** | Basic `CELERY_AVAILABLE` flag | Actual Redis ping test |

---

## Configuration Details

### Backend Main Application (`backend/main.py`)

```python
# 1. Load Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 2. Test connection and initialize Celery
try:
    import redis
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()  # Verify connection
    
    celery_app = Celery('algoviz', broker=REDIS_URL, backend=REDIS_URL)
    CELERY_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Celery/Redis not available: {e}")
    CELERY_AVAILABLE = False

# 3. Root endpoint returns actual Redis status
@app.get("/")
async def root():
    redis_status = False
    if CELERY_AVAILABLE:
        try:
            redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            redis_client.ping()
            redis_status = True
        except Exception as e:
            redis_status = False
    
    return {
        "message": "Algorithm Visualization API",
        "celery_available": CELERY_AVAILABLE,
        "redis_available": redis_status,
        "redis_url": f"{REDIS_URL[:40]}...",
        "version": "1.0.0"
    }
```

### Celery Worker (`backend/celery_worker.py`)

```python
# 1. Load Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 2. Initialize Celery with Redis broker
app = Celery(
    'algoviz',
    broker=REDIS_URL,
    backend=REDIS_URL
)

# 3. Configure for Upstash SSL
app.conf.update(
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_pool_limit=None,  # Upstash requires this
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Enable SSL for rediss:// protocol
    broker_use_ssl=REDIS_URL.startswith('rediss://'),
    redis_backend_use_ssl={...} if REDIS_URL.startswith('rediss://') else {},
)
```

---

## Upstash Redis Setup

### What is Upstash Redis?

- **Cloud-hosted Redis** with SSL/TLS encryption
- **Serverless** - scales automatically
- **Fully managed** - no maintenance needed
- **Use `rediss://` protocol** for SSL connections

### Your Redis Connection

```
Protocol:   rediss://  (with SSL)
Host:       guiding-minnow-44165.upstash.io
Port:       6379
Username:   default
Password:   AayFAAIncDE3MDRiNWNmMzRjMWY0OGUxYWFjNzA5NDk1ZmZhYTUzZHAxNDQxNjU
Full URL:   rediss://default:AayFAAIncDE3MDRiNWNmMzRjMWY0OGUxYWFjNzA5NDk1ZmZhYTUzZHAxNDQxNjU@guiding-minnow-44165.upstash.io:6379
```

### Environment Variable on Render

```
Name:   REDIS_URL
Value:  rediss://default:AayFAAIncDE3MDRiNWNmMzRjMWY0OGUxYWFjNzA5NDk1ZmZhYTUzZHAxNDQxNjU@guiding-minnow-44165.upstash.io:6379
```

---

## SSL/TLS Configuration

### Why `rediss://`?

- **`redis://`** = No encryption (for localhost only)
- **`rediss://`** = With SSL/TLS encryption (for remote, recommended for production)

### Upstash SSL Handling

The configuration automatically enables SSL when the URL starts with `rediss://`:

```python
broker_use_ssl=REDIS_URL.startswith('rediss://'),
```

**No additional certificates needed!** Upstash handles SSL transparently.

---

## How It Works

### 1. Startup Flow

```
Application starts
  ↓
Load REDIS_URL from environment
  ↓
Create Redis client: redis.from_url(REDIS_URL)
  ↓
Test connection: redis_client.ping()
  ↓
If success:
  ✅ Initialize Celery with Redis broker
  ✅ Set CELERY_AVAILABLE = True
Else:
  ⚠️  Fall back to synchronous execution
  ⚠️  Set CELERY_AVAILABLE = False
```

### 2. Root Endpoint (`GET /`)

When you call `https://algoviz-backend-ytfh.onrender.com/`:

```json
{
  "message": "Algorithm Visualization API",
  "celery_available": true,
  "redis_available": true,
  "redis_url": "rediss://default:Aay...@guiding-minnow...",
  "version": "1.0.0"
}
```

### 3. Task Processing

```
Frontend triggers task
  ↓
Celery task enqueued to Redis
  ↓
Worker picks up task from Redis
  ↓
Executes render_algorithm task
  ↓
Result stored in Redis
  ↓
Frontend polls /task-status/{task_id}
  ↓
Task result retrieved from Redis
```

---

## Testing Redis Connection

### Test 1: Check Root Endpoint

```bash
curl https://algoviz-backend-ytfh.onrender.com/
```

**Successful response:**
```json
{
  "message": "Algorithm Visualization API",
  "celery_available": true,
  "redis_available": true,
  "...": "..."
}
```

**If `redis_available` is `false`:**
- Check `REDIS_URL` environment variable on Render
- Verify URL is exactly correct (no typos)
- Check Upstash console for connection details
- Verify Upstash Redis instance is running

### Test 2: Direct Redis Connection (Local Dev)

```bash
# Test local Redis
redis-cli ping
# Should return: PONG

# Test Upstash Redis
redis-cli -u rediss://default:PASSWORD@guiding-minnow-44165.upstash.io:6379 ping
# Should return: PONG
```

### Test 3: Celery Worker Status

```bash
# Start Celery worker
celery -A celery_worker worker --loglevel=info

# You should see:
# Connected to rediss://...@guiding-minnow...
# 
# ▽ celery v5.6.2
#   ...
```

---

## Environment Variables

### On Render Dashboard

Navigate to: **Service → Settings → Environment Variables**

```
REDIS_URL=rediss://default:AayFAAIncDE3MDRiNWNmMzRjMWY0OGUxYWFjNzA5NDk1ZmZhYTUzZHAxNDQxNjU@guiding-minnow-44165.upstash.io:6379
GEMINI_API_KEY=your_gemini_key
ALLOWED_ORIGINS=https://algoviz-frontend.vercel.app
```

### Local Development (`.env`)

```
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_gemini_key
```

---

## Dependencies

All required packages are already in `requirements.txt`:

```
celery==5.6.2
redis==7.2.0
```

No additional installation needed! ✅

---

## Troubleshooting

### Issue: `redis_available: false` in root endpoint

**Cause:** Redis connection failed

**Debug steps:**
```bash
# 1. Check REDIS_URL is set
echo $REDIS_URL  # Should show your Redis URL

# 2. Test connection manually
redis-cli -u "REDIS_URL_HERE" ping

# 3. Check Render logs
# Render Dashboard → Service → Logs
# Look for connection errors
```

**Solutions:**
- Verify `REDIS_URL` is correct (copy from Upstash console)
- Ensure no trailing spaces in URL
- Check Upstash Redis instance is running (not paused)
- Verify network/firewall allows connection

### Issue: Celery worker won't start

**Error:** `ConnectionError: Error 104 connecting to ...`

**Cause:** Wrong Redis URL or connection timeout

**Fix:**
```bash
# 1. Verify URL locally
redis-cli -u "REDIS_URL" ping

# 2. Check Upstash console for valid credentials

# 3. Restart Upstash instance if paused

# 4. Add retry configuration (already in code)
CELERY_BROKER_CONNECTION_RETRY=True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
```

### Issue: Slow task processing

**Cause:** Network latency or Upstash limits

**Check:**
- Upstash dashboard for concurrent connections
- Render and Upstash region proximity
- Task complexity and timeout settings

---

## Celery Task Example

### Define a Task (`backend/celery_worker.py`)

```python
@app.task(name="render_algorithm")
def render_algorithm(plan):
    topic = plan.get("topic", "")
    task_id = plan.get("task_id", "default")
    # ... render logic
    return {"status": "completed", "video_url": f"media/{task_id}.mp4"}
```

### Enqueue a Task (`backend/main.py`)

```python
from celery_worker import app as celery_app

@app.post("/render")
async def trigger_render(plan: dict):
    if CELERY_AVAILABLE:
        # Async task via Redis
        result = celery_app.send_task('render_algorithm', args=[plan])
        return {"task_id": result.id, "status": "queued"}
    else:
        # Sync fallback
        result = render_algorithm_sync(plan)
        return result
```

---

## Performance Notes

### Upstash vs Local Redis

| Aspect | Local | Upstash |
|--------|-------|---------|
| **Latency** | <1ms | 10-50ms |
| **Reliability** | Depends on machine | ✅ 99.99% SLA |
| **SSL** | Manual setup | Automatic |
| **Scaling** | Limited | Automatic |
| **Cost** | Free but hardware cost | Pay-as-you-go |

### Optimization for Render ↔ Upstash

- Upstash and Render are optimized for low-latency connections ✅
- Connection pooling enabled (`broker_pool_limit=None`)
- Retry logic enabled for reliability ✅
- Task serialization optimized (JSON)

---

## Production Checklist

- [ ] `REDIS_URL` set in Render environment variables
- [ ] Redis URL starts with `rediss://` (SSL enabled)
- [ ] Root endpoint returns `redis_available: true`
- [ ] Celery worker can connect (no connection errors in logs)
- [ ] Tasks queued and processed successfully
- [ ] Monitor Upstash dashboard for usage

---

## Monitoring

### Upstash Console

Visit: https://console.upstash.com

View:
- ✅ Real-time commands being executed
- ✅ Memory usage and limits
- ✅ Connection count
- ✅ Latency metrics

### Render Logs

Go to: **Service → Logs**

Look for:
- ✅ `✅ Celery configured with Redis: rediss://...`
- ✅ `✅ SSL enabled: True`
- ❌ Connection errors (would show here)

---

## Summary

✅ **Celery configured with Upstash Redis**  
✅ **SSL/TLS encryption enabled**  
✅ **Root endpoint pings Redis for actual status**  
✅ **Fallback to synchronous if Redis unavailable**  
✅ **Ready for asynchronous task processing**  

Your backend can now handle:
- ✅ Asynchronous long-running Manim renders
- ✅ Distributed task processing
- ✅ Scalable algorithm visualization
- ✅ Real-time task status monitoring

**All via remote Upstash Redis with SSL encryption!** 🎉
