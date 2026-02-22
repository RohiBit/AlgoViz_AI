# 404 Error Route Matching Guide - AlgoViz AI

## ✅ Routes Verified & Matching

All endpoint routes are **correctly named and matching** between frontend and backend:

### Frontend → Backend Route Mapping

| Frontend Call | HTTP Method | Backend Route | Status |
|---------------|-------------|---------------|--------|
| `apiClient.post('/generate-plan')` | POST | `@app.post("/generate-plan")` | ✅ MATCH |
| `apiClient.post('/render')` | POST | `@app.post("/render")` | ✅ MATCH |
| `apiClient.get('/task-status/{id}')` | GET | `@app.get("/task-status/{task_id}")` | ✅ MATCH |
| `apiClient.get('/pipeline-status/{id}')` | GET | `@app.get("/pipeline-status/{task_id}")` | ✅ MATCH |
| `apiClient.post('/visualize-code-execution')` | POST | `@app.post("/visualize-code-execution")` | ✅ MATCH |
| `apiClient.post('/upload-vision')` | POST | `@app.post("/upload-vision")` | ✅ MATCH |

**All routes match perfectly!** ✅ No `/api` prefix needed.

---

## Possible Causes of 404 Error

### 1️⃣ **API_URL is Incorrect** (Most Likely)

Check `frontend/src/services/api.ts`:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

**Verify:**
```bash
# Your deployed backend URL
https://algoviz-backend-ytfh.onrender.com
```

**Does your Vercel environment have?**
```
VITE_API_URL=https://algoviz-backend-ytfh.onrender.com
```

If missing or wrong, it falls back to `http://localhost:8000` → **404 on production**.

### 2️⃣ **Backend Not Responding**

Test backend availability:
```bash
curl -v https://algoviz-backend-ytfh.onrender.com/

# Should see:
< HTTP/1.1 200 OK
{"message": "Algorithm Visualization API", "celery_available": false}
```

**If 404:**
- Render backend is down
- Wrong URL

### 3️⃣ **CORS Error Masked as 404**

In browser DevTools:
1. Open **Network** tab
2. Click "Visualize"
3. Look for request to `/generate-plan`
4. Check **Response** tab for error message
5. Check **Headers** tab for `Access-Control-Allow-Origin`

If CORS error: See [CORS_SETUP.md](../CORS_SETUP.md)

### 4️⃣ **Trailing Slashes** 

❌ **Wrong:**
```typescript
apiClient.post('/generate-plan/')  // Extra slash
```

✅ **Correct:**
```typescript
apiClient.post('/generate-plan')   // No trailing slash
```

Current frontend is correct! ✅

---

## Debugging Steps

### Step 1: Test Backend Health

```bash
# Test if backend is running
curl https://algoviz-backend-ytfh.onrender.com/

# Should return:
# {"message": "Algorithm Visualization API", "celery_available": false}
```

### Step 2: Test Route Directly

```bash
# Test /generate-plan endpoint
curl -X POST https://algoviz-backend-ytfh.onrender.com/generate-plan \
  -H "Content-Type: application/json" \
  -d '{"topic": "bubble-sort", "intent": "text", "user_input": ""}'

# Should return a teaching plan (not 404)
```

### Step 3: Check Browser Network Tab

1. Open **DevTools** (F12)
2. Go to **Network** tab
3. Click "Visualize" button
4. Look for the `POST /generate-plan` request
5. Check:
   - **URL**: Is it your correct backend URL?
   - **Status**: 404 or 200?
   - **Response**: Error message?
   - **Headers**: `Access-Control-Allow-Origin` present?

### Step 4: Check Frontend Environment Variable

In Vercel dashboard, verify:

```
Settings → Environment Variables → VITE_API_URL
```

Should be:
```
https://algoviz-backend-ytfh.onrender.com
```

If not present, frontend will use `http://localhost:8000` → **404 in production**.

### Step 5: Check Render Logs

In Render dashboard:

```
Your Service → Logs
```

Look for:
- `INFO: Started server process [1]` ✅ (Running)
- `INFO: Uvicorn running on http://0.0.0.0:8000` ✅ (Listening)
- Any error messages ❌

---

## Quick Fix Checklist

- [ ] **Vercel has `VITE_API_URL` set to your Render backend**
- [ ] **Run `npm run build` locally** to test build
- [ ] **Backend is responding** at `https://algoviz-backend-ytfh.onrender.com/`
- [ ] **No trailing slashes** in API routes
- [ ] **CORS configured** (see CORS_SETUP.md)
- [ ] **Vercel redeployed** after setting environment variable

---

## Common 404 Scenarios

### Scenario 1: Environment Variable Not Set in Vercel

```
Frontend code:
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  
Vercel setting:
  VITE_API_URL = (not set)
  
Result:
  Frontend tries: http://localhost:8000 → 404 (no local server)
```

**Fix:**
1. Vercel Dashboard → Settings → Environment Variables
2. Add: `VITE_API_URL=https://algoviz-backend-ytfh.onrender.com`
3. Redeploy

### Scenario 2: Wrong Backend URL

```
Correct: https://algoviz-backend-ytfh.onrender.com
Wrong:   https://algoviz-backend.onrender.com (missing ID)
Wrong:   http://algoviz-backend-ytfh.onrender.com (http instead of https)
```

**Fix:** Copy exact URL from Render dashboard

### Scenario 3: Render Backend Down

```
curl https://algoviz-backend-ytfh.onrender.com/
→ Connection refused or 503 Service Unavailable
```

**Fix:**
1. Check Render dashboard → Logs
2. Restart service if needed
3. Check for deployment errors

---

## Complete Route Documentation

### `POST /generate-plan`

**Frontend:**
```typescript
const response = await apiClient.post('/generate-plan', {
  topic: input,
  intent: mode,
  user_input: input
});
```

**Backend:**
```python
@app.post("/generate-plan")
async def generate_plan(request: VisualRequest):
    plan = generate_teaching_plan_with_gemini(request.topic)
    return plan
```

**Returns:**
```json
{
  "task_id": "uuid",
  "topic": "bubble-sort",
  "steps": [...],
  "estimatedDuration": 180,
  "createdAt": "uuid"
}
```

---

### `POST /render`

**Frontend:**
```typescript
const response = await apiClient.post('/render', {
  task_id: plan.id,
  topic: plan.topic,
  steps: plan.steps
});
```

**Backend:**
```python
@app.post("/render")
async def trigger_render(plan: dict):
    task_id = plan.get("task_id")
    result = render_algorithm_sync(plan)
    return {...}
```

**Returns:**
```json
{
  "status": "completed|failed",
  "task_id": "uuid",
  "video_url": "media/uuid.mp4",
  "plan": {...}
}
```

---

### `GET /task-status/{task_id}`

**Frontend:**
```typescript
const response = await apiClient.get(`/task-status/${taskId}`);
```

**Backend:**
```python
@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    video_path = f"media/{task_id}.mp4"
    if os.path.exists(video_path):
        return {"task_id": task_id, "status": "SUCCESS", ...}
    else:
        return {"task_id": task_id, "status": "PENDING"}
```

---

### `GET /pipeline-status/{task_id}`

**Frontend:**
```typescript
const response = await apiClient.get(`/pipeline-status/${taskId}`);
```

**Backend:**
```python
@app.get("/pipeline-status/{task_id}")
async def get_pipeline_status(task_id: str):
    # Returns pipeline stages with status
```

**Returns:**
```json
{
  "task_id": "uuid",
  "current_stage": 1,
  "stages": [
    {"id": 1, "label": "...", "status": "completed"},
    {...}
  ],
  "status": "PROCESSING|SUCCESS"
}
```

---

## Summary

✅ **All routes are correctly named and matching**  
✅ **No `/api` prefix needed**  
✅ **No trailing slashes**  

**Most likely cause of 404:**
- ❓ **Environment variable `VITE_API_URL` not set in Vercel**
- ❓ **Backend is offline or unreachable**
- ❓ **CORS is blocking the request** (check browser console)

**Next steps:**
1. Verify `VITE_API_URL` in Vercel settings
2. Test backend: `curl https://algoviz-backend-ytfh.onrender.com/`
3. Check browser DevTools → Network tab
4. Check browser console for errors
