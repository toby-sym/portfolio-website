# Portfolio Website Setup & Running Guide

## Quick Start (Local Development)

### Prerequisites
- macOS/Linux/Windows with zsh or bash
- Python 3.9+
- Node.js 16+ & npm

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend
cd backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# The default .env already configured for local SQLite development
# No changes needed unless you want to customize
```

### 2. Frontend Setup (3 minutes)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Done! Ready to run
```

---

## Running Locally

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --port 8001 --reload
```

Output:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Status**: Backend is ready at http://localhost:8001

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Output:
```
  VITE v5.4.21  ready in 366 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Status**: Frontend is ready at http://localhost:5173

---

## First Time Setup

### Initialize Database (one-time)

```bash
# Backend must be running first
curl -X POST http://localhost:8001/init

# Expected response:
# {
#   "detail": "Admin user created successfully",
#   "username": "admin",
#   "user_id": 1
# }
```

This creates the default admin user so you can start adding projects.

---

## Testing the Full Stack

### 1. Visit Frontend
Go to http://localhost:5173 in your browser

### 2. Navigate to Admin Login
Click "Admin Login" in the navigation

### 3. Login with Default Credentials
- Username: `admin`
- Password: `admin`

### 4. Add a Test Project
- Click "Admin" in navigation
- Click "+ Add New Project"
- Fill in the form:
  - **Title**: "My First Project"
  - **Description**: "A test of the new portfolio system"
  - **Technologies**: "FastAPI, Svelte, PostgreSQL"
  - **GitHub Link**: https://github.com/toby-sym
  - Check "Featured Project"
- Click "Create Project"

### 5. View on Public Side
- Click "Projects" in navigation
- You should see your newly created project!

---

## .env Configuration

### Backend (.env file in `backend/` folder)

```env
# Database Connection
# For local SQLite (development)
DATABASE_URL=sqlite:///./test_portfolio.db

# For PostgreSQL (production on Render)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production-1234567890

# Admin Credentials (change after first login!)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin

# Server Port (optional, default 8000)
PORT=8000
```

### Frontend (.env.local file in `frontend/` folder - Optional)

Create `.env.local` if you want custom API URL:

```env
VITE_API_URL=http://localhost:8001
```

Leave unset to use default (`http://localhost:8001`).

For production:
```env
VITE_API_URL=https://your-render-backend.onrender.com
```

---

## Stopping Services

### Graceful Shutdown
- Backend: Press `CTRL+C` in terminal
- Frontend: Press `CTRL+C` in terminal

### Clean Restart
```bash
# Clear SQLite database (start fresh)
cd backend
rm -f test_portfolio.db

# Run init again
# (after restarting backend)
curl -X POST http://localhost:8001/init
```

---

## Useful URLs During Development

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | Svelte development server |
| Backend API | http://localhost:8001 | REST API |
| API Docs | http://localhost:8001/docs | Interactive Swagger UI |
| Health Check | http://localhost:8001/health | API status |

---

## Common Issues & Solutions

### Issue: "Port already in use"
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9

# Or use different port
python -m uvicorn main:app --port 8002
```

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: npm command not found
```bash
# Check Node installation
node --version
npm --version

# Install Node.js from https://nodejs.org/
```

### Issue: "ENOENT: no such file or directory"
```bash
# Ensure you're in correct directory
pwd  # Should show .../portfolio-website/backend or .../frontend

# List files to verify
ls -la
```

### Issue: Projects not showing after creation
- Verify backend is running
- Check browser console for JS errors
- Clear browser cache (Cmd+Shift+Delete)
- Check if Admin Dashboard actually created project

### Issue: Login always fails
- Verify `.env` username/password match
- Check database initialization (`/init` endpoint)
- Look at backend terminal for error messages

---

## Development Workflow

### Adding New Features

1. **Backend Changes**
   - Edit files in `backend/`
   - Backend auto-reloads (with `--reload` flag)
   - Check http://localhost:8001/docs for updated API

2. **Frontend Changes**
   - Edit `.svelte` files in `frontend/src/`
   - Frontend auto-reloads (Vite hot reload)
   - Changes visible instantly in browser

### Testing an API Endpoint

```bash
# Get all projects
curl http://localhost:8001/projects

# Create a project (need valid JWT token)
curl -X POST http://localhost:8001/projects \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Test",
    "description":"Test project",
    "technologies":"Test"
  }'

# Check API documentation
# Open http://localhost:8001/docs in browser
```

---

## Building for Production

### Frontend Build
```bash
cd frontend
npm run build
# Creates optimized files in dist/ folder
npm run preview  # Test production build locally
```

### Backend Production Checklist
- [ ] Update `SECRET_KEY` in `.env`
- [ ] Change `ADMIN_PASSWORD` in `.env`
- [ ] Restrict `CORS` origins in `settings.py`
- [ ] Switch from SQLite to PostgreSQL
- [ ] Upgrade password hashing to bcrypt
- [ ] Review all environment variables
- [ ] Test with `DATABASE_URL` pointing to PostgreSQL

---

## Project Layout Explanation

```
backend/
├── main.py                 # FastAPI routes & initialization
├── models.py               # Database tables (Project, User)
├── auth.py                 # Login & JWT logic
├── schemas.py              # API request/response structure
├── database.py             # Database connection setup
├── settings.py             # Read .env configuration
├── requirements.txt        # Python package list
└── test_portfolio.db       # SQLite database (created auto)

frontend/
├── src/
│   ├── App.svelte          # Main app component (navigation)
│   ├── api.js              # HTTP client for backend
│   └── pages/
│       ├── Home.svelte     # About page
│       ├── Projects.svelte # List projects from API
│       ├── Contact.svelte  # Contact info
│       ├── AdminLogin.svelte    # Login form
│       └── AdminDashboard.svelte # Manage projects
├── vite.config.js          # Build configuration
├── package.json            # JavaScript dependencies
└── dist/                   # Production build (after `npm run build`)
```

---

## Next Steps

1. ✅ Run local setup (you're here!)
2. ✅ Test admin login & project creation
3. ⬜ Deploy backend to Render
4. ⬜ Deploy frontend to GitHub Pages
5. ⬜ Update production domain in frontend
6. ⬜ Add existing projects via admin
7. ⬜ Update portfolio content (email, links, etc.)

See `IMPLEMENTATION_SUMMARY.md` for detailed deployment steps.

---

## Getting Help

### Check API Status
```bash
curl http://localhost:8001/health
# Should return: {"status":"ok"}
```

### View Backend Logs
- Watch terminal where you ran `npm run dev` (frontend)
- Watch terminal where you ran `python uvicorn ...` (backend)

### Browser Developer Tools
- F12 → Console tab for JavaScript errors
- F12 → Network tab to see API calls
- F12 → Application → Storage for localStorage (tokens)

### Backend Documentation
- Auto-generated: http://localhost:8001/docs (Swagger UI)
- Interactive API testing built-in

---

Happy coding! 🚀
