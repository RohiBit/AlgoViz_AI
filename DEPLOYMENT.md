# AlgoViz AI - Production Deployment Guide

## Overview
This guide covers deploying **AlgoViz AI** with:
- **Frontend**: Vercel (React + Vite + TypeScript)
- **Backend**: Render (FastAPI + Manim + Celery)

---

## Prerequisites

### Local Development
- Python 3.11+
- Node.js 18+
- Git
- FFmpeg (for Manim video rendering)

### Accounts Required
- [GitHub](https://github.com)
- [Vercel](https://vercel.com) (frontend hosting)
- [Render](https://render.com) (backend hosting)
- [Google AI Studio](https://aistudio.google.com/app/apikeys) (Gemini API key)

---

## Step 1: Secure Your API Keys

### 1.1 Backend (.env)

Create `backend/.env` with your actual credentials:

```env
# Gemini API Key (get from: https://aistudio.google.com/app/apikeys)
GEMINI_API_KEY=your_actual_key_here

# Production Origins (comma-separated)
ALLOWED_ORIGINS=https://algoviz-frontend.vercel.app

# Redis (if using Celery)
REDIS_URL=your_redis_url_here

# Environment
ENVIRONMENT=production
```

**CRITICAL**: Never commit `.env` files to Git. They're in `.gitignore`.

### 1.2 Frontend (.env.local, .env.production)

**For local development** (`frontend/.env.local`):
```env
VITE_API_URL=http://localhost:8000
```

**For production** (set in Vercel dashboard):
```
VITE_API_URL=https://algoviz-backend.onrender.com
```

---

## Step 2: Deploy Backend to Render

### 2.1 Create Render Account & New Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository

### 2.2 Configure Render Service

**Settings:**
- **Name**: `algoviz-backend`
- **Environment**: `Python 3.11`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Root Directory**: `backend`

### 2.3 Set Environment Variables in Render

In Render Dashboard → Your Service → **Environment**:

```
GEMINI_API_KEY=your_actual_key
ALLOWED_ORIGINS=https://algoviz-frontend.vercel.app
ENVIRONMENT=production
```

### 2.4 Deploy
- Push to GitHub or click **"Deploy"** in Render dashboard
- Wait for deployment (~5-10 minutes)
- Your backend URL: `https://algoviz-backend.onrender.com`

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account & New Project
1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Import your GitHub repository
3. Select `frontend` as the root directory

### 3.2 Configure Vercel Project

**Build Settings:**
- **Framework**: Vite
- **Build Command**: `npm run build`
- **Install Command**: `npm ci`
- **Output Directory**: `dist`

### 3.3 Set Environment Variables in Vercel

In Vercel Dashboard → Your Project → **Settings → Environment Variables**:

```
VITE_API_URL=https://algoviz-backend.onrender.com
```

### 3.4 Deploy
- Vercel will auto-deploy on Git push
- Your frontend URL: `https://algoviz-frontend.vercel.app`

---

## Step 4: Connect Frontend & Backend

### Update Backend CORS
The CORS is already configured in `backend/main.py`:

```python
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Local dev
    "https://algoviz-frontend.vercel.app",  # Production
]
```

If you need more origins, add them to Render's `ALLOWED_ORIGINS` env variable:
```
ALLOWED_ORIGINS=https://algoviz-frontend.vercel.app,https://yourdomain.com
```

### Verify Connection
1. Open your frontend: `https://algoviz-frontend.vercel.app`
2. Submit an algorithm
3. Check browser DevTools → Network tab to verify API calls go to your Render backend

---

## Step 5: Add Custom Domain (Optional)

### For Vercel (Frontend)
1. **Vercel Dashboard** → Your Project → **Settings → Domains**
2. Add your domain (e.g., `algoviz.com`)
3. Update DNS records provided by Vercel

### For Render (Backend)
1. **Render Dashboard** → Your Service → **Settings → Custom Domain**
2. Add subdomain (e.g., `api.algoviz.com`)
3. Update DNS records

---

## Troubleshooting

### Issue: "CORS error" when frontend calls backend
**Solutions:**
1. Verify `VITE_API_URL` is correct in frontend
2. Check Render env variables: `ALLOWED_ORIGINS` must include frontend URL
3. Restart Render service after updating env vars

### Issue: Backend 404 when accessing `/generate-plan`
**Solutions:**
1. Verify backend is running: Open `https://algoviz-backend.onrender.com/docs`
2. Check `main.py` is in `backend/` directory (Render root setting)
3. Verify `uvicorn` is installed in `requirements.txt`

### Issue: Frontend shows blank page or build error
**Solutions:**
1. Check Vercel build logs: **Deployments → Select deployment → Logs**
2. Verify `npm run build` works locally: `cd frontend && npm run build`
3. Check Node.js version: `nvm use 18` or higher

### Issue: Gemini API errors
**Solutions:**
1. Verify API key at [aistudio.google.com](https://aistudio.google.com/app/apikeys)
2. Check API key in Render env variables (no extra spaces)
3. Ensure Gemini API is enabled in Google Cloud console

---

## Production Checklist

- [ ] API keys are in `.env` files (NOT in code)
- [ ] `.env` files are in `.gitignore`
- [ ] Render env variables are set
- [ ] Vercel env variables are set
- [ ] CORS origins are configured correctly
- [ ] Backend URL in frontend matches Render service
- [ ] `requirements.txt` is up-to-date: `pip freeze > requirements.txt`
- [ ] Test frontend → backend API calls in production
- [ ] Monitor Render logs for errors
- [ ] Set up error tracking (optional: Sentry, etc.)

---

## Helpful Links

- [Render Documentation](https://docs.render.com)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI CORS Docs](https://fastapi.tiangolo.com/tutorial/cors/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Google Gemini API](https://ai.google.dev/)
