# Complete 404 Debugging Guide - AlgoViz AI

## Understanding Your 404 Error

The 404 error when clicking "Visualize" happens because your browser cannot reach one of these endpoints:
- ❌ `https://algoviz-backend-ytfh.onrender.com/generate-plan`
- ❌ `https://algoviz-backend-ytfh.onrender.com/render`
- ❌ `https://algoviz-backend-ytfh.onrender.com/task-status/{taskId}`

We've verified these routes **exist and match perfectly** in your FastAPI backend ✅

**The real cause is likely:**
1. Frontend doesn't know the backend URL (missing `VITE_API_URL` env var)
2. Backend is unreachable (offline/deploying)
3. CORS is blocking the request
4. Network connectivity issue

---

## Step 1: Identify the Failing Request

### Using Chrome DevTools:

1. **Open your Vercel frontend** in browser
2. Press **F12** to open DevTools
3. Go to **Network** tab
4. Click **Visualize** button
5. Look for a failed request with RED status code

### What to look for:

```
Request URL:  (This is KEY!)
Method:       POST or GET
Status:       404 ❌ or 200 ✅
```

**Example failing request:**
```
URL: http://localhost:8000/generate-plan  ← WRONG! Using local URL
Status: 404 Not Found
```

**Example working request:**
```
URL: https://algoviz-backend-ytfh.onrender.com/generate-plan
Status: 200 OK
```

---

## Step 2: Check Browser Console for Errors

1. **DevTools** → **Console** tab
2. Look for error messages (usually red)
3. Click to expand error

### Common Errors:

```javascript
// Error 1: CORS Error (not 404, but related)
Access to XMLHttpRequest at 'https://...' from origin 'https://...' 
has been blocked by CORS policy

// Error 2: Network Error (backend unreachable)
TypeError: Failed to fetch
NetworkError: A network error occurred.

// Error 3: 404 Not Found (route doesn't exist)
POST https://algoviz-backend-ytfh.onrender.com/generate-plan 404 (Not Found)

// Error 4: Wrong API URL (missing env var)
POST http://localhost:8000/generate-plan 404 (Not Found)
```

---

## Step 3: The Critical Check - Is VITE_API_URL Set?

This is the **#1 cause** of 404 errors in your app.

### Check Vercel Environment Variables:

1. Go to [Vercel Dashboard](https://vercel.com/projects)
2. Click your **algovizfrontend** project
3. **Settings** → **Environment Variables**
4. Look for: `VITE_API_URL`

### Scenarios:

#### ✅ **CORRECT** - Variable is set
```
Name:  VITE_API_URL
Value: https://algoviz-backend-ytfh.onrender.com
```

Frontend will use: `https://algoviz-backend-ytfh.onrender.com/generate-plan` ✅

#### ❌ **WRONG** - Variable missing (MOST COMMON)
```
(VITE_API_URL not in list)
```

Frontend defaults to: `http://localhost:8000/generate-plan`  
Result: 404 from Vercel ❌

#### ❌ **WRONG** - Variable has incorrect value
```
Name:  VITE_API_URL
Value: https://algoviz-backend.onrender.com  ← Missing ID
```

Frontend tries: `https://algoviz-backend.onrender.com/generate-plan`  
Result: 404 (URL doesn't exist) ❌

---

## Step 4: Verify Backend URL

If VITE_API_URL is set correctly, verify the backend actually exists:

```bash
# Test if backend is alive
curl https://algoviz-backend-ytfh.onrender.com/

# Should return:
# {"message": "Algorithm Visualization API", "celery_available": false}
```

**If timeout or connection error:**
- Render backend is offline
- Check Render dashboard
- Restart service if needed

**If 404:**
- URL is wrong
- Copy exact URL from Render dashboard

---

## Step 5: Test the Route Directly

Once you verify backend is alive, test the specific route:

```bash
curl -X POST https://algoviz-backend-ytfh.onrender.com/generate-plan \
  -H "Content-Type: application/json" \
  -d '{"topic": "bubble-sort", "intent": "text", "user_input": ""}'
```

**Should return** (not 404):
```json
{
  "task_id": "some-uuid",
  "topic": "bubble-sort",
  "steps": [...],
  "estimatedDuration": 180,
  "createdAt": "some-uuid"
}
```

**If 404:**
- Route doesn't exist on backend
- Check `/generate-plan` is spelled exactly right
- Verify backend deployed with latest code

---

## Step 6: Inspect Network Request Details

In DevTools → Network tab:

1. **Find failed request** in list
2. **Click on it**
3. Check these tabs:

### Headers Tab:
```
Request URL: https://algoviz-backend-ytfh.onrender.com/generate-plan
Request Method: POST
Status Code: 404 Not Found
```

### Request Tab:
```json
{
  "topic": "bubble-sort",
  "intent": "text",
  "user_input": ""
}
```

### Response Tab:
```html
<html>
  <head><title>404 Not Found</title></head>
  <body>...</body>
</html>
```

If response is HTML with "404", the route truly doesn't exist.

---

## Case Sensitivity - Critical for Linux!

Render backend runs on Linux, which **IS case-sensitive**.

❌ **WRONG:**
```typescript
apiClient.post('/Generate-Plan')      // Capital G and P
apiClient.post('/generate-plan/')     // Trailing slash
```

✅ **CORRECT:**
```typescript
apiClient.post('/generate-plan')      // Exact case match
```

**Current code is correct!** ✅

---

## URL Structure Verification

Your frontend code uses:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const response = await apiClient.post('/generate-plan', {...})
```

This creates URL:
```
Base:  https://algoviz-backend-ytfh.onrender.com
Path:  /generate-plan
Full:  https://algoviz-backend-ytfh.onrender.com/generate-plan
```

✅ **This is correct!**

---

## Debugging Decision Tree

```
↓ Click "Visualize"
↓ Error appears?

If ERROR shows "404":
  ↓
  Check DevTools → Network
  ↓
  What's the Request URL?
  ├─ http://localhost:8000/generate-plan?
  │  └─ PROBLEM: VITE_API_URL not set in Vercel
  │     FIX: Set it (see below)
  │
  ├─ https://algoviz-backend-ytfh.onrender.com/generate-plan?
  │  └─ PROBLEM: Backend is unreachable
  │     FIX: Check Render dashboard / backend logs
  │
  └─ https://different-url.onrender.com/generate-plan?
     └─ PROBLEM: Wrong URL in VITE_API_URL
        FIX: Update to correct Render URL

Else if ERROR shows CORS error:
  └─ Not a 404, see CORS_SETUP.md

Else if no ERROR:
  └─ Success! Backend working
```

---

## The Quick Fix (Most Likely Solution)

### 1. Go to Vercel
```
https://vercel.com/projects → algovizfrontend → Settings → Environment Variables
```

### 2. Add/Update Variable
```
Name:  VITE_API_URL
Value: https://algoviz-backend-ytfh.onrender.com
```

### 3. Redeploy
```bash
# Either:
git push                          # Auto-redeploy

# Or click Redeploy in Vercel dashboard
# Or wait for Vercel to auto-detect the env var change
```

### 4. Test Again
Open Vercel frontend → Click Visualize → Check Network tab → Should be 200! ✅

---

## Summary Checklist

- [ ] Open DevTools (F12)
- [ ] Go to Network tab
- [ ] Click Visualize
- [ ] Look for 404 request
- [ ] Check Request URL - is it correct?
  - [ ] If `http://localhost:8000` → Set `VITE_API_URL` in Vercel
  - [ ] If wrong URL → Update `VITE_API_URL` in Vercel
  - [ ] If correct URL but 404 → Check backend logs
- [ ] Check Console tab for error messages
- [ ] Test backend: `curl https://algoviz-backend-ytfh.onrender.com/`
- [ ] Test route: `curl -X POST https://algoviz-backend-ytfh.onrender.com/generate-plan -H "Content-Type: application/json" -d '...'`
- [ ] Redeploy Vercel after changes
- [ ] Hard refresh browser (Ctrl+Shift+R)

---

## Reference Links

- Frontend source: `frontend/src/services/api.ts` (lines 1-20)
- Backend routes: `backend/main.py` (lines 252-480)
- [Vercel Env Variables Docs](https://vercel.com/docs/concepts/projects/environment-variables)
- [DevTools Network Tab Guide](https://developer.chrome.com/docs/devtools/network/)

---

## Still Stuck?

1. **Take a screenshot** of the failed Network request
2. **Copy the Request URL** from the Headers tab
3. **Verify** it matches your Render backend URL
4. **Check** if VITE_API_URL is in Vercel settings
5. **Restart** backend if needed
6. **Redeploy** frontend with environment variable set
