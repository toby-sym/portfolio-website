# Portfolio API - FastAPI Backend

Modern REST API built with FastAPI for a portfolio website with admin authentication and project management.

## Features

- 🔐 JWT-based admin authentication
- 📋 Project CRUD endpoints (Create, Read, Update, Delete)
- 🔒 Protected admin routes
- 📊 PostgreSQL database
- 🚀 Ready for production deployment on Render/Railway
- 📚 Auto-generated API documentation (Swagger UI)

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (or SQLite for development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib

## Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (or use SQLite for quick testing)

### Installation

1. **Create virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or with Poetry:
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and credentials
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
   
   Server will be available at: `http://localhost:8000`

### Local Database Setup (PostgreSQL)

#### Option A: Using PostgreSQL locally
```bash
# Create database
createdb portfolio_db

# Update DATABASE_URL in .env:
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio_db
```

#### Option B: Quick Testing with SQLite
```bash
# Update DATABASE_URL in .env:
DATABASE_URL=sqlite:///./portfolio.db
```

### First Time Setup

After starting the server, initialize the database with admin user:
```bash
curl -X POST http://localhost:8000/init
```

This creates the default admin user (credentials from `.env`).

## API Endpoints

### Swagger Documentation
Visit `http://localhost:8000/docs` for interactive API documentation

### Health Check
- `GET /health` — Check API status

### Authentication
- `POST /auth/login` — Login with credentials, returns JWT token
  ```bash
  curl -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin"}'
  ```

- `GET /auth/me` — Get current user info (requires auth token)

### Projects (Public)
- `GET /projects` — Get all projects (public)
- `GET /projects/{id}` — Get specific project (public)

### Projects (Admin - Requires Authentication)
- `POST /projects` — Create new project
- `PUT /projects/{id}` — Update project
- `DELETE /projects/{id}` — Delete project

### Using Authentication
Include the token in the `Authorization` header:
```bash
curl -X POST http://localhost:8000/projects \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "description": "Description here",
    "technologies": "Python, FastAPI",
    "github_link": "https://github.com/...",
    "featured": true
  }'
```

## Project Structure

```
backend/
├── main.py              # FastAPI app and route definitions
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response models
├── database.py          # Database connection and session management
├── auth.py              # JWT token and password utilities
├── settings.py          # Configuration from environment variables
├── requirements.txt     # Python dependencies (pip)
├── pyproject.toml       # Poetry project configuration
├── Procfile             # Render/Heroku deployment config
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Deployment to Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial backend setup"
git push origin main
```

### Step 2: Create PostgreSQL Database on Render
1. Go to [Render.com](https://render.com)
2. Create new PostgreSQL database
3. Copy the database URL

### Step 3: Create Web Service on Render
1. Create new Web Service
2. Connect your GitHub repository
3. Set environment variables:
   ```
   DATABASE_URL=<your_render_postgres_url>
   SECRET_KEY=<generate_a_strong_secret>
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=<change_this_to_strong_password>
   ```
4. Build command: `pip install -r requirements.txt` (or `poetry install`)
5. Start command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

### Step 4: Initialize Database
After deployment, run:
```bash
curl -X POST https://your-render-app.onrender.com/init
```

## Testing

### Run tests:
```bash
pytest
```

### Manual API testing with curl or Postman:
1. Visit `http://localhost:8000/docs` (Swagger UI)
2. Click "Try it out" on any endpoint
3. Fill in parameters and execute

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/db` |
| `SECRET_KEY` | JWT signing secret (keep secure!) | `your-secret-key-min-32-chars` |
| `ADMIN_USERNAME` | Default admin username | `admin` |
| `ADMIN_PASSWORD` | Default admin password | `changeme123` |
| `CORS_ORIGINS` | Allowed origins for CORS | `["http://localhost:5173", "https://example.com"]` |

## Security Notes

⚠️ **Important for Production:**
1. Change `SECRET_KEY` to a strong, random value (32+ characters)
2. Change `ADMIN_PASSWORD` immediately after first login
3. Set `CORS_ORIGINS` to specific domains (not `*`)
4. Use HTTPS only
5. Keep `.env` and private keys out of version control
6. Implement rate limiting for auth endpoints
7. Use environment-specific settings

## Troubleshooting

**Connection refused to database:**
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify database exists and credentials match

**"Invalid token" errors:**
- Token may have expired (default: 7 days)
- Re-login to get new token
- Check token format: `Authorization: Bearer <token>`

**Port already in use:**
```bash
# Use different port:
uvicorn main:app --port 8001
```

## Next Steps

1. ✅ Backend API complete
2. Build Svelte frontend (`/frontend` directory)
3. Create admin dashboard UI
4. Deploy frontend
5. Connect and test end-to-end

## License

MIT
