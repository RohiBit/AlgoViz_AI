# 404 Error - Immediate Action Plan

## ✅ Route Verification Complete

All FastAPI routes **match frontend API calls perfectly:**

```
✅ POST /generate-plan matches
✅ POST /render matches
✅ GET /task-status/{id} matches
✅ GET /pipeline-status/{id} matches
✅ POST /visualize-code-execution matches
✅ POST /upload-vision matches
```

**No `/api` prefix needed. No trailing slashes.**

---

## 🔴 Most Likely Cause: Missing Environment Variable

Your **Vercel frontend** doesn't know how to reach your **Render backend**.

### Check This Right Now:

1. **Go to**: [Vercel Dashboard](https://vercel.com) → Your Project → Settings → Environment Variables

2. **Look for**: `VITE_API_URL`

   - **If NOT there** → That's your problem! ❌
   - **If there** → Check the value:
     ```
     https://algoviz-backend-ytfh.onrender.com  ✅ Correct
     http://localhost:8000                       ❌ Wrong (local URL)
     https://algoviz-backend.onrender.com        ❌ Wrong (missing ID)
     ```

---

## 🔧 Quick Fix (5 minutes)

### Step 1: Add Environment Variable to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/account/projects)
2. Click on **algovizfrontend** project
3. Click **Settings** → **Environment Variables**
4. Click **Add New**
5. Fill in:
   ```
   Name:  VITE_API_URL
   Value: https://algoviz-backend-ytfh.onrender.com
   ```
6. Click **Save**

### Step 2: Redeploy Vercel

Option A (Automatic):
```bash
git push  # Vercel auto-deploys on git push
```

Option B (Manual):
1. Go to **Deployments** tab in Vercel
2. Click **Redeploy** on latest deployment
3. Wait for "Ready" status

---

## ✅ Verification Steps

After setting environment variable and redeploying:

### Test 1: Backend Is Alive
```bash
curl https://algoviz-backend-ytfh.onrender.com/
```

Should return:
```json
{"message": "Algorithm Visualization API", "celery_available": false}
```

### Test 2: Route Exists
```bash
curl -X POST https://algoviz-backend-ytfh.onrender.com/generate-plan \
  -H "Content-Type: application/json" \
  -d '{"topic": "bubble-sort", "intent": "text", "user_input": ""}'
```

Should return a teaching plan (not 404).

### Test 3: Frontend Can Reach Backend

1. Open Vercel frontend: `https://algovizfrontend-*.vercel.app`
2. Open **DevTools** (F12)
3. Go to **Network** tab
4. Click "Visualize"
5. Look for `POST /generate-plan` request
6. Check:
   - **Status**: 200 (not 404)
   - **URL**: Has your backend URL?
   - **Response**: Data (not error)?

---

## 🐛 If Still Getting 404

### Debug Path:

1. **Check Vercel build logs:**
   - Deployments → Click deployment → Logs
   - Look for errors during build

2. **Check Vercel runtime logs:**
   - Deployments → Click deployment → Runtime Logs
   - Should show network requests

3. **Browser DevTools Network tab:**
   - Right-click failed request
   - Copy as cURL
   - Run to see full error

4. **Render backend logs:**
   - Go to Render dashboard
   - Your service → Logs
   - Should show incoming POST requests
   - If no requests: frontend isn't reaching it

---

## 📋 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Frontend shows 404 | Env var not set | Set `VITE_API_URL` in Vercel |
| Frontend uses localhost | Env var is `http://localhost:8000` | Update to `https://algoviz-backend-ytfh.onrender.com` |
| Vercel shows 404 | Frontend didn't redeploy | Click Redeploy in Vercel |
| POST request fails silently | CORS error (check console) | See CORS_SETUP.md |
| Backend says 404 | Route doesn't exist | Check backend route name matches |

---

## 📞 Still Stuck?

Follow this debugging flow:

```
1. Can you reach backend?
   curl https://algoviz-backend-ytfh.onrender.com/
   
   YES → Continue to 2
   NO  → Render backend is down
   
2. Is VITE_API_URL set in Vercel?
   Vercel Settings → Environment Variables
   
   YES → Continue to 3
   NO  → SET IT NOW (see Quick Fix above)
   
3. Has Vercel redeployed?
   Deployments → Status should be "Ready"
   
   YES → Continue to 4
   NO  → Click Redeploy
   
4. Check browser Network tab
   (F12 → Network → Click Visualize)
   
   Status 200? → Success! ✅
   Status 404? → Route mismatch (check ROUTE_DEBUGGING.md)
   CORS error? → See CORS_SETUP.md
```

---

## 📚 Reference Docs

- [ROUTE_DEBUGGING.md](./ROUTE_DEBUGGING.md) - Complete route documentation
- [CORS_SETUP.md](./CORS_SETUP.md) - CORS configuration
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide

---

**Next Action**: Set `VITE_API_URL` in Vercel and redeploy. That will fix the 404! 🚀
