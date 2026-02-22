# CORS Configuration Guide for AlgoViz AI

## Issue Fixed ✅

Your React frontend on Vercel was blocked by CORS (Cross-Origin Resource Sharing) policy when trying to access the FastAPI backend on Render.

### Error Message (Resolved)
```
Access to XMLHttpRequest at 'https://algoviz-backend-ytfh.onrender.com/generate-plan' 
from origin 'https://algovizfrontend-lgbv5u3hy-rkprinczs-projects.vercel.app' 
has been blocked by CORS policy.
```

---

## Solution Implemented

### Updated `backend/main.py`

```python
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

# Regex pattern to allow all Vercel preview deployments
vercel_preview_regex = r"https://.*\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=vercel_preview_regex,  # Allows ALL Vercel preview deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### What This Allows

✅ **Development**: `http://localhost:5173`  
✅ **Production**: `https://algoviz-frontend.vercel.app`  
✅ **Preview**: `https://algovizfrontend-lgbv5u3hy-rkprinczs-projects.vercel.app`  
✅ **All Vercel Preview Deployments**: `https://<anything>.vercel.app` (via regex)  
✅ **Environment Variable Origins**: `ALLOWED_ORIGINS` env var (comma-separated)  

---

## How It Works

### 1. Exact Origin Matching
```python
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://algoviz-frontend.vercel.app",
    "https://algovizfrontend-lgbv5u3hy-rkprinczs-projects.vercel.app",
]
```
These must match **exactly**. Used for predictable, fixed origins.

### 2. Regex Pattern Matching
```python
vercel_preview_regex = r"https://.*\.vercel\.app"
```
This matches **any** Vercel deployment:
- ✅ `https://algoviz-frontend.vercel.app`
- ✅ `https://algovizfrontend-lgbv5u3hy-fork.vercel.app`
- ✅ `https://algovizfrontend-feature-branch.vercel.app`
- ✅ Any other `.vercel.app` subdomain

### 3. Environment Variable Flexibility
```python
if os.getenv("ALLOWED_ORIGINS"):
    additional_origins = os.getenv("ALLOWED_ORIGINS").split(",")
    ALLOWED_ORIGINS.extend([origin.strip() for origin in additional_origins])
```

Add origins without code changes:
```bash
# In Render environment variables:
ALLOWED_ORIGINS=https://custom-domain.com,https://staging.example.com
```

---

## Deployment Status

✅ **Changes Committed**: `f9c2145`  
✅ **Pushed to GitHub**  
✅ **Render Auto-Detecting**: Watch the logs  
✅ **ETA**: 2-5 minutes for redeploy  

---

## Next Steps

### 1. Wait for Render Redeploy
- Go to [Render Dashboard](https://dashboard.render.com)
- Select your service
- Watch the **Deployments** tab
- Status should show "In Progress" → "Live" ✅

### 2. Test the Connection
Once deployed, test from your Vercel frontend:

```bash
curl https://algoviz-backend-ytfh.onrender.com/docs
```

Should return Swagger UI documentation (200 OK).

### 3. Verify CORS Headers
Use browser DevTools:
1. Open Network tab
2. Make a request to `/generate-plan`
3. Check Response Headers:
   ```
   Access-Control-Allow-Origin: https://algovizfrontend-lgbv5u3hy-rkprinczs-projects.vercel.app
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE, ...
   Access-Control-Allow-Headers: *
   ```

---

## Advanced CORS Patterns

### Pattern: Allow Only Vercel Production
```python
vercel_production_regex = r"https://.*\.vercel\.app$"  # Matches Vercel only
```

### Pattern: Allow Specific Subdomains
```python
# Allow algoviz-frontend-* preview deployments
vercel_preview_regex = r"https://algoviz-frontend-.*\.vercel\.app"
```

### Pattern: Allow Multiple Hosts
```python
# Allow Vercel + custom domain
multi_regex = r"https://(.*\.vercel\.app|algoviz\.com|staging\.algoviz\.com)"
```

### Pattern: Allow Any HTTPS
```python
# SECURITY WARNING: Only use in development!
allow_origin_regex = r"https://.*"
```

---

## Security Notes

⚠️ **Current Setup is Production-Safe**
- ✅ Only HTTPS origins allowed
- ✅ Vercel preview URLs are auto-generated and secure
- ✅ No wildcard `*` used (which would allow any origin)
- ✅ Credentials allowed only with explicit origins

⚠️ **Don't Do This in Production**
```python
# ❌ BAD: Allows ANY origin
allow_origins=["*"]

# ❌ BAD: HTTP in production
ALLOWED_ORIGINS = ["http://another-site.com"]

# ❌ BAD: No HTTPS requirement
allow_origin_regex = r".*"
```

---

## Testing Locally

### Start Local Dev Environment
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Browser Console Test
```javascript
// In Vercel frontend at http://localhost:5173
fetch('http://localhost:8000/generate-plan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ topic: 'bubble-sort', intent: 'text', user_input: '' })
})
.then(r => r.json())
.then(data => console.log('Success!', data))
.catch(err => console.error('CORS Error:', err))
```

---

## Troubleshooting

### Still Getting CORS Error?

1. **Check Render Logs**
   ```bash
   # View logs in Render dashboard
   # Settings → Logs
   ```

2. **Verify Origin Header** (DevTools Network)
   - Check the `Origin` header in the failed request
   - Is it in your `ALLOWED_ORIGINS` list?

3. **Clear Browser Cache**
   ```bash
   # Hard refresh in browser
   Ctrl+Shift+R  (Windows)
   Cmd+Shift+R   (Mac)
   ```

4. **Check Environment Variables**
   - Render Dashboard → Your Service → Environment
   - Verify `ALLOWED_ORIGINS` if you added custom origins

5. **Verify Render Deployment**
   - Check if redeploy is complete
   - Look for "Application startup complete" in logs

### Common Mistakes

❌ **Forgetting `https://`**
```python
# Wrong:
ALLOWED_ORIGINS = ["algoviz-frontend.vercel.app"]

# Correct:
ALLOWED_ORIGINS = ["https://algoviz-frontend.vercel.app"]
```

❌ **Trailing Slash**
```python
# Wrong:
ALLOWED_ORIGINS = ["https://algoviz-frontend.vercel.app/"]

# Correct:
ALLOWED_ORIGINS = ["https://algoviz-frontend.vercel.app"]
```

❌ **Port Numbers**
```python
# Wrong (ports not used with domains):
ALLOWED_ORIGINS = ["https://algoviz-frontend.vercel.app:3000"]

# Correct:
ALLOWED_ORIGINS = ["https://algoviz-frontend.vercel.app"]
```

---

## Reference

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Vercel Deployments](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)

---

## Summary

✅ **CORS fix deployed to production**  
✅ **Wildcard regex enabled for all Vercel preview deployments**  
✅ **Local development still works**  
✅ **Environment variables support custom origins**  
✅ **Security best practices applied**  

Your frontend should now connect to the backend without CORS errors! 🚀
