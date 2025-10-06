# 🚀 Deployment Guide

Complete guide to deploy the Pokemon Card Price Checker to production.

## Quick Deployment (Recommended)

### Backend: Render
### Frontend: Vercel

---

## 📦 Backend Deployment (Render)

### Step 1: Prepare Your Repository

Make sure all files are committed:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy to Render

1. **Go to [Render](https://render.com/)** and sign up/login with GitHub

2. **Click "New +" → "Web Service"**

3. **Connect Your Repository**
   - Select your GitHub repository
   - Name: `pokemon-card-price-checker-backend`
   - Region: Oregon (or closest to you)
   - Branch: `main`

4. **Configure Build Settings**
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

5. **Set Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Add: `OPENAI_API_KEY` = `your-actual-api-key`
   - Add: `PORT` = `10000` (Render sets this automatically)
   - Add: `DEBUG` = `False`

6. **Choose Plan**
   - Select **Free** plan
   - Click "Create Web Service"

7. **Wait for Deployment**
   - Render will automatically build and deploy
   - Takes ~5 minutes
   - You'll get a URL like: `https://pokemon-card-price-checker-backend.onrender.com`

### Step 3: Test Your Backend

```bash
# Test health endpoint
curl https://your-backend-url.onrender.com/

# Test API docs
# Visit: https://your-backend-url.onrender.com/docs
```

### ⚠️ Important Notes for Render:

- **Free tier sleeps after 15 min of inactivity** - First request after sleep takes ~30 seconds
- **750 hours/month free** - Enough for development/demo
- **Automatic deploys** - Every git push to main automatically deploys

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Update Frontend API URL

Before deploying, update the backend URL in your frontend:

```bash
# Edit frontend/app.js
# Change this line:
const API_BASE_URL = 'http://localhost:8000';

# To your Render backend URL:
const API_BASE_URL = 'https://your-backend-url.onrender.com';
```

Commit the change:
```bash
git add frontend/app.js
git commit -m "Update API URL for production"
git push origin main
```

### Step 2: Deploy to Vercel

**Option A: Using Vercel CLI (Recommended)**

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to your project root
cd /path/to/AI-Lodge---Pokemon-Card-Price-Checker

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? pokemon-card-price-checker
# - In which directory is your code? ./frontend
# - Override settings? No

# Deploy to production
vercel --prod
```

**Option B: Using Vercel Dashboard**

1. **Go to [Vercel](https://vercel.com/)** and sign up/login with GitHub

2. **Click "Add New..." → "Project"**

3. **Import Your Repository**
   - Find and select your GitHub repo
   - Click "Import"

4. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: Leave empty (static site)
   - **Output Directory**: Leave empty
   - Click "Deploy"

5. **Wait for Deployment**
   - Takes ~1 minute
   - You'll get a URL like: `https://pokemon-card-price-checker.vercel.app`

### Step 3: Update Backend URL (Again)

After getting your Vercel URL, you may want to update the frontend to use environment variables:

1. In Vercel dashboard → Your Project → Settings → Environment Variables
2. Add: `VITE_API_URL` = `https://your-backend-url.onrender.com`
3. Redeploy

---

## 🎯 Alternative Deployment Options

### Backend Alternatives

#### 1. **Railway** (Similar to Render)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
cd backend
railway init

# Deploy
railway up

# Add environment variables
railway variables set OPENAI_API_KEY=your-key
```

#### 2. **Heroku**
```bash
# Install Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Create app
heroku create pokemon-card-backend

# Set buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key

# Deploy
git push heroku main
```

#### 3. **AWS Lambda + API Gateway** (Advanced)
- Use [Mangum](https://mangum.io/) adapter for FastAPI
- More complex but highly scalable
- Free tier: 1M requests/month

### Frontend Alternatives

#### 1. **Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod
```

#### 2. **GitHub Pages**
```bash
# In your repo settings:
# Settings → Pages → Source → main branch → /frontend folder
```

#### 3. **Cloudflare Pages**
- Connect GitHub repo
- Build directory: `frontend`
- Automatic deployments

---

## 🔧 Post-Deployment Configuration

### Update CORS (if needed)

If you want to restrict CORS to only your frontend domain:

```python
# backend/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pokemon-card-price-checker.vercel.app",
        "http://localhost:3000",  # For local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Set Up Custom Domain (Optional)

**Vercel:**
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

**Render:**
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records

---

## 📊 Monitoring & Logs

### Render Logs
- Dashboard → Your Service → Logs
- Real-time logs of requests and errors

### Vercel Logs
- Dashboard → Your Project → Deployments → View Function Logs
- Shows all requests and errors

---

## 🐛 Common Deployment Issues

### Backend Issues

**Issue: Build fails with "No module named 'fastapi'"**
```bash
# Solution: Ensure requirements.txt is in backend directory
# Check: backend/requirements.txt exists
```

**Issue: 500 Internal Server Error**
```bash
# Solution: Check environment variables
# Verify OPENAI_API_KEY is set in Render dashboard
```

**Issue: Backend sleeps after 15 min (Render Free)**
```bash
# Solution: 
# 1. Upgrade to paid plan ($7/month)
# 2. Use cron job to ping every 10 minutes
# 3. Accept 30s cold start on first request
```

### Frontend Issues

**Issue: API requests fail with CORS error**
```bash
# Solution: Verify API_BASE_URL is correct
# Check browser console for actual error
# Ensure backend CORS allows your domain
```

**Issue: Images not loading**
```bash
# Solution: Check assets folder is included in deployment
# Verify path in CSS: url('./assets/pokemon-background.png')
```

**Issue: Environment variables not working**
```bash
# Solution: Vercel needs variables prefixed with VITE_
# Redeploy after adding variables
```

---

## ✅ Deployment Checklist

Before deploying:
- [ ] All code committed and pushed to GitHub
- [ ] `.env` file NOT committed (in .gitignore)
- [ ] OpenAI API key ready
- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] CORS configured correctly

After backend deployment:
- [ ] Backend URL obtained
- [ ] Backend health check works
- [ ] API docs accessible at `/docs`
- [ ] Environment variables set

After frontend deployment:
- [ ] Frontend URL obtained
- [ ] Frontend loads correctly
- [ ] Can upload images
- [ ] Backend connection works
- [ ] Card identification works

---

## 🚀 Deployment Commands Summary

```bash
# Backend (Render) - via Dashboard
# 1. Connect GitHub repo
# 2. Set root directory to 'backend'
# 3. Add OPENAI_API_KEY environment variable
# 4. Deploy

# Frontend (Vercel) - via CLI
npm install -g vercel
cd /path/to/project
vercel --prod

# Or use dashboard:
# 1. Import GitHub repo
# 2. Set root directory to 'frontend'
# 3. Deploy
```

---

## 💰 Cost Breakdown

### Free Tier (Development/Demo)
- **Render Backend**: Free (with sleep after 15 min)
- **Vercel Frontend**: Free (100GB bandwidth/month)
- **OpenAI API**: Pay per use (~$0.01-0.03 per card)
- **Total**: ~$0-5/month depending on usage

### Paid Tier (Production)
- **Render Backend**: $7/month (always on)
- **Vercel Frontend**: Free or $20/month (Pro)
- **OpenAI API**: ~$10-50/month depending on traffic
- **Total**: ~$17-77/month

---

## 📝 Next Steps After Deployment

1. **Share your app!** 🎉
2. Monitor usage and errors
3. Set up analytics (Google Analytics, Plausible)
4. Add more features
5. Apply for TCGPlayer API for real pricing
6. Consider adding authentication
7. Set up monitoring/alerts

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **GitHub Issues**: Open an issue in your repo

---

**Your app will be live at:**
- 🔗 Backend: `https://your-app.onrender.com`
- 🔗 Frontend: `https://your-app.vercel.app`

Good luck with your deployment! 🚀
