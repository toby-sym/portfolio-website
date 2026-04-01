# Render Deployment Guide

## Overview
Your backend is ready to deploy to Render with your existing PostgreSQL database. This guide walks you through connecting Render to GitHub and setting environment variables.

## Prerequisites
- ✅ GitHub repository pushed (just done)
- ✅ Render PostgreSQL database created (already set up)
- ✅ Render account (sign up at https://render.com)

---

## Step 1: Connect GitHub to Render (One-time setup)

1. Go to https://render.com and log in
2. Click **"New +"** → **"Web Service"**
3. Select **"Build and deploy from a Git repository"**
4. Click **"Connect account"** next to GitHub
5. Authorize Render to access your GitHub repositories
6. Click **"Connect"** on your `portfolio-website` repository

---

## Step 2: Configure Web Service

### Basic Settings
| Setting | Value |
|---------|-------|
| **Name** | `portfolio-website` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app` |
| **Instance Type** | Free (or Starter for more stability) |

### Root Path Configuration
- **Root Directory**: `backend` (Deploy from backend folder)

---

## Step 3: Set Environment Variables

Click **"Advanced"** and add the following environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | `postgresql://portfolio_website_sqpp_user:2gcAnLUqu5qlk8hc4cAdw5Prkb10yMwt@dpg-d76kkbhr0fns73cd3lr0-a.frankfurt-postgres.render.com/portfolio_website_sqpp` | Your existing database connection |
| `SECRET_KEY` | `68ab69b9d35b7a74924063571564d32e64374b266aa592440f84c62ece38993f` | Already set in code; can be regenerated for security |
| `ADMIN_USERNAME` | `admin` | Change after first login |
| `ADMIN_PASSWORD` | `changeme123` | **IMPORTANT: Change this immediately!** |
| `CORS_ORIGINS` | `["http://localhost:5173","https://toby-sym.github.io"]` | Update for production domains |
| `PORT` | `(leave blank - Render sets automatically)` | Render assigns port dynamically |

⚠️ **Security Warning**: After first successful deployment:
1. Change ADMIN_PASSWORD to a strong password
2. Regenerate SECRET_KEY: `python3 -c "import secrets; print(secrets.token_hex(32))"`
3. Update these in Render environment variables
4. Restart the service

---

## Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment to complete (2-3 minutes)
3. You'll see your service URL: `https://portfolio-website.onrender.com`

### Monitor Deployment
- Watch the **"Logs"** tab to see build progress
- Look for: `"Application startup complete"` → Deployment succeeded ✅
- If errors appear, check the logs for troubleshooting

---

## Step 5: Initialize Database on Render

Once deployment is complete and service is running:

```bash
# Initialize database tables and admin user
curl -X POST https://portfolio-website.onrender.com/init

# Check that it worked
curl https://portfolio-website.onrender.com/health
# Should return: {"status":"ok"}
```

---

## Step 6: Test Deployed Backend

```bash
# Test 1: Health check
curl https://portfolio-website.onrender.com/health

# Test 2: Login (get JWT token)
TOKEN=$(curl -s -X POST https://portfolio-website.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"changeme123"}' | jq -r '.access_token')

# Test 3: Fetch projects
curl https://portfolio-website.onrender.com/projects

# Test 4: Create a project (with token from Test 2)
curl -X POST https://portfolio-website.onrender.com/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Your Project",
    "description": "Project description",
    "technologies": "Tech 1, Tech 2",
    "github_link": "https://github.com/...",
    "live_link": "https://...",
    "featured": true
  }'
```

---

## Step 7: Update Frontend to Use Deployed Backend

Once backend is live on Render:

### For Local Development:
```bash
cd frontend
echo "VITE_API_URL=https://portfolio-website.onrender.com" > .env.local
npm run dev
```

### For Production (GitHub Pages):
Update [frontend/src/api.js](frontend/src/api.js) line ~6:
```javascript
const BASE_URL = import.meta.env.VITE_API_URL || 'https://portfolio-website.onrender.com';
```

Then build and deploy frontend to GitHub Pages.

---

## Step 8: Configure Custom Domain (Optional)

If you want to use a custom domain instead of `.onrender.com`:

1. In Render dashboard, click your service
2. Go to **"Settings"** → **"Custom Domains"**
3. Add your domain
4. Update your DNS settings as instructed
5. Update `CORS_ORIGINS` environment variable with your custom domain

---

## Troubleshooting

### Service won't start / "Application startup complete" doesn't appear

**Possible causes:**
1. **Missing DATABASE_URL**: Check environment variables
2. **Connection refused**: Verify PostgreSQL database is accessible
3. **Wrong Python version**: Ensure Python 3.9+ is used

**Solution:**
- Check **Logs** tab in Render for error messages
- Verify DATABASE_URL is correctly set
- Test database connection locally: `python backend/main.py`

### "Port already in use" error

- This won't happen on Render (it assigns the port)
- Only happens locally; kill process: `lsof -ti:8001 | xargs kill -9`

### CORS errors in frontend

- Verify CORS_ORIGINS includes your frontend domain
- Restart service after changing environment variables

### Database errors ("relation does not exist")

- Run POST /init endpoint again: `curl -X POST https://your-service.onrender.com/init`
- This recreates tables if they're missing

### Admin login fails

- Verify ADMIN_PASSWORD matches what's set in Render environment
- If changed, restart service and run POST /init again

---

## Security Checklist Before Going to Production

- [ ] Change ADMIN_PASSWORD to a strong password
- [ ] Generate new SECRET_KEY and update in Render
- [ ] Restrict CORS_ORIGINS to your domain only
- [ ] Review database credentials (already protected in connection string)
- [ ] Enable HTTPS (Render does this automatically)
- [ ] Monitor Render logs regularly

---

## Next Steps

1. **Deploy to Render** using steps above
2. **Update frontend** to point to deployed backend URL
3. **Deploy frontend** to GitHub Pages
4. **Test end-to-end**: Create project via admin dashboard, see it on public site
5. **Add your projects** via admin panel at `https://yourdomain.com/admin`

---

## Useful Commands

```bash
# View backend logs from command line (if Render CLI installed)
render logs --name portfolio-website

# Test backend health from anywhere
curl https://portfolio-website.onrender.com/health

# Generate new SECRET_KEY for rotation
python3 -c "import secrets; print(secrets.token_hex(32))"

# Backup all projects from live backend
curl https://portfolio-website.onrender.com/projects > projects_backup.json
```

---

## Support

- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **PostgreSQL Connection**: https://www.postgresql.org/docs/current/libpq-connstring.html

---

**Status**: Backend code committed and pushed ✅  
**Next**: Follow steps 1-8 to deploy to Render
