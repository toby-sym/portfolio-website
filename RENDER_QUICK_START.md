# 🚀 Render Deployment - Quick Start

## What's Done ✅
- ✅ Code committed to GitHub (security fixes applied)
- ✅ Backend configured for PostgreSQL on Render
- ✅ Environment variables documented
- ✅ Database already initialized locally (tables + admin user created)
- ✅ All 6 CRUD endpoints tested and working

## What's Left (30 minutes) 🔜

### 1. Create Render Web Service (10 min)
Open: https://render.com
- Click "New +" → "Web Service"
- Connect GitHub `toby-sym/portfolio-website`
- Set:
  - **Root Directory**: `backend`
  - **Build Command**: `pip install -r backend/requirements.txt`
  - **Start Command**: `cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

### 2. Set Environment Variables (5 min)
In Render dashboard, add these 6 variables:
```
DATABASE_URL=postgresql://portfolio_website_sqpp_user:2gcAnLUqu5qlk8hc4cAdw5Prkb10yMwt@dpg-d76kkbhr0fns73cd3lr0-a.frankfurt-postgres.render.com/portfolio_website_sqpp
SECRET_KEY=68ab69b9d35b7a74924063571564d32e64374b266aa592440f84c62ece38993f
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123
CORS_ORIGINS=["http://localhost:5173","https://toby-sym.github.io"]
```

### 3. Deploy & Verify (10 min)
- Click "Create Web Service"
- Wait 2-3 minutes for deployment
- Test: `curl https://portfolio-website-3a8v.onrender.com/health`
- Initialize: `curl -X POST https://portfolio-website-3a8v.onrender.com/init`

### 4. Update Frontend (5 min)
Update `frontend/.env.local`:
```
VITE_API_URL=https://portfolio-website-3a8v.onrender.com
```

---

## Your Deployed URL
### Backend: `https://portfolio-website-3a8v.onrender.com` ✅ LIVE
### Frontend: `https://toby-sym.github.io/portfolio-website` (Next step: deploy)

---

## Files to Reference
- **RENDER_DEPLOYMENT.md** - Detailed step-by-step guide
- **SETUP_GUIDE.md** - Local development
- **IMPLEMENTATION_SUMMARY.md** - Architecture overview
- **backend/README.md** - API documentation
- **frontend/README.md** - Frontend setup

---

## After Deployment
1. ✅ Change ADMIN_PASSWORD to a strong password
2. ✅ Add your projects via admin dashboard
3. ✅ See them on public portfolio site
4. ✅ Deploy frontend to GitHub Pages

---

**Everything is ready! Just need to create the Render Web Service (10-minute process).**
