# Vercel Deployment Guide - Connect Frontend to Backend

## 🚨 Current Problem

Your deployed frontend on Vercel is trying to connect to `http://localhost:8000`, which doesn't work because:

1. **localhost is local** - Vercel's servers can't access your local machine
2. **You need a public URL** for your backend that Vercel can reach

---

## ✅ Solutions (Choose One)

### Option 1: Use Ngrok (Quick Demo - Recommended for Hackathon)

**Best for:** Quick demos, hackathon presentations, testing

**Steps:**

1. **Install Ngrok**
   - Download from: https://ngrok.com/download
   - Or: `npm install -g ngrok` (if you have npm)

2. **Start Your Backend**
   ```bash
   # In your project directory
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start Ngrok Tunnel**
   ```bash
   # In a new terminal
   ngrok http 8000
   ```

4. **Copy the Public URL**
   ```
   Ngrok will show something like:
   
   Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
   
   Copy: https://abc123.ngrok-free.app
   ```

5. **Set Vercel Environment Variable**
   - Go to: https://vercel.com/dashboard
   - Select your project: `thorax-spoon-os`
   - Go to: Settings → Environment Variables
   - Add new variable:
     - **Name:** `NEXT_PUBLIC_BACKEND_URL`
     - **Value:** `https://abc123.ngrok-free.app` (your ngrok URL)
     - **Environment:** Production, Preview, Development (select all)
   - Click "Save"

6. **Redeploy**
   - Go to: Deployments tab
   - Click "Redeploy" on latest deployment
   - Or push a new commit to trigger deployment

7. **Test**
   - Visit: https://thorax-spoon-os.vercel.app
   - Should now connect to your backend!

**⚠️ Important:**
- Ngrok URL changes every time you restart (free plan)
- You'll need to update Vercel env var each time
- Keep ngrok running during demo/presentation

---

### Option 2: Deploy Backend to Cloud (Production - Best Long-term)

**Best for:** Production deployment, permanent solution

**Platforms:**

#### A. Railway (Easiest)
1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys
6. Copy the public URL (e.g., `https://thorax-backend.railway.app`)
7. Set in Vercel env vars

#### B. Render (Free Tier)
1. Go to: https://render.com
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy and copy URL
7. Set in Vercel env vars

#### C. Heroku
1. Go to: https://heroku.com
2. Create new app
3. Connect GitHub repository
4. Add Python buildpack
5. Deploy
6. Copy URL and set in Vercel

---

### Option 3: Mock Backend (Demo Only - Not Recommended)

**Best for:** Frontend-only demo when backend is down

Create a mock API that returns fake data. Not recommended for hackathon since you want to show real functionality.

---

## 🔧 Setting Vercel Environment Variables

### Via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - URL: https://vercel.com/dashboard
   - Find project: `thorax-spoon-os`

2. **Navigate to Settings**
   - Click on your project
   - Click "Settings" tab
   - Click "Environment Variables" in sidebar

3. **Add Variable**
   - **Key:** `NEXT_PUBLIC_BACKEND_URL`
   - **Value:** Your backend URL (ngrok or deployed backend)
   - **Environments:** Check all (Production, Preview, Development)
   - Click "Save"

4. **Redeploy**
   - Go to "Deployments" tab
   - Click "..." menu on latest deployment
   - Click "Redeploy"
   - Wait for build to complete

### Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Set environment variable
vercel env add NEXT_PUBLIC_BACKEND_URL

# When prompted, enter your backend URL
# Select: Production, Preview, Development

# Redeploy
vercel --prod
```

---

## 🎯 Quick Setup for Hackathon Demo

**Recommended approach for your presentation:**

### Step 1: Install Ngrok
```bash
# Download from https://ngrok.com/download
# Or install via npm
npm install -g ngrok
```

### Step 2: Start Backend
```bash
# Terminal 1
cd c:\Users\Admin\Documents\aol-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Start Ngrok
```bash
# Terminal 2
ngrok http 8000

# Copy the HTTPS URL shown (e.g., https://abc123.ngrok-free.app)
```

### Step 4: Update Vercel
```bash
# Go to: https://vercel.com/dashboard
# Project: thorax-spoon-os
# Settings → Environment Variables
# Add: NEXT_PUBLIC_BACKEND_URL = https://abc123.ngrok-free.app
# Save and Redeploy
```

### Step 5: Test
```bash
# Visit: https://thorax-spoon-os.vercel.app
# Should work now!
```

---

## 🔍 Troubleshooting

### Issue 1: "ERR_BLOCKED_BY_CLIENT"

**Cause:** Ad blocker or browser extension blocking requests

**Fix:**
- Disable ad blocker for your site
- Try incognito/private mode
- Check browser console for actual error

### Issue 2: "CORS Error"

**Cause:** Backend not allowing requests from Vercel domain

**Fix:** Update backend CORS settings

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://thorax-spoon-os.vercel.app",
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 3: "Failed to fetch"

**Cause:** Backend URL is wrong or backend is down

**Fix:**
- Verify backend is running
- Check ngrok tunnel is active
- Verify Vercel env var is correct
- Check backend URL in browser

### Issue 4: "Ngrok URL keeps changing"

**Cause:** Free ngrok plan generates new URL each restart

**Fix:**
- Upgrade to ngrok paid plan for static domain
- Or deploy backend to cloud platform
- Or use ngrok config file:

```bash
# Create ngrok.yml
authtoken: YOUR_AUTH_TOKEN
tunnels:
  thorax:
    proto: http
    addr: 8000

# Run with config
ngrok start thorax
```

---

## 📊 Environment Variable Reference

### Frontend (.env.local)
```env
# Local development
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### Vercel (Production)
```env
# Option 1: Ngrok (temporary)
NEXT_PUBLIC_BACKEND_URL=https://abc123.ngrok-free.app

# Option 2: Deployed backend (permanent)
NEXT_PUBLIC_BACKEND_URL=https://thorax-backend.railway.app

# Option 3: Custom domain
NEXT_PUBLIC_BACKEND_URL=https://api.thorax.com
```

---

## ✅ Verification Checklist

Before your presentation:

- [ ] Backend is running locally
- [ ] Ngrok tunnel is active
- [ ] Ngrok HTTPS URL copied
- [ ] Vercel env var set to ngrok URL
- [ ] Vercel redeployed
- [ ] Frontend loads without errors
- [ ] Can register contract
- [ ] Can view AI analysis
- [ ] Can send alerts
- [ ] Real-time logs working

---

## 🎤 For Hackathon Presentation

**30 minutes before:**
1. Start backend: `uvicorn app.main:app --reload`
2. Start ngrok: `ngrok http 8000`
3. Copy ngrok URL
4. Update Vercel env var
5. Redeploy Vercel
6. Test everything works
7. Keep both terminals running during presentation

**During presentation:**
- Use Vercel URL: https://thorax-spoon-os.vercel.app
- Backend runs on your laptop via ngrok
- Judges see professional deployed frontend
- Everything works in real-time

**Backup plan:**
- Have screenshots ready
- Have video recording of working demo
- Can fall back to localhost demo if needed

---

## 🚀 Quick Commands

```bash
# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start ngrok
ngrok http 8000

# Check if backend is accessible
curl http://localhost:8000/health

# Check if ngrok is working
curl https://YOUR-NGROK-URL.ngrok-free.app/health

# Redeploy Vercel
vercel --prod
```

---

## 📞 Quick Reference

**Problem:** Frontend can't connect to backend

**Cause:** localhost URL doesn't work in production

**Solution:** Use ngrok to create public URL

**Steps:**
1. `ngrok http 8000`
2. Copy HTTPS URL
3. Set in Vercel env vars
4. Redeploy

**Time:** 5 minutes

---

**Your frontend will work perfectly for the demo! 🚀**

