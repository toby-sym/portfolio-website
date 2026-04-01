from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta

from database import engine, get_db, Base
from settings import settings
from models import Project, User
from schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user,
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio API",
    description="Backend API for portfolio website with admin panel",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint. Returns JWT token for admin access.
    
    Default credentials (change in production):
    - username: admin
    - password: admin
    """
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return {"access_token": access_token}


@app.get("/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info."""
    return current_user


# ============================================================================
# Project Endpoints - Public
# ============================================================================

@app.get("/projects", response_model=list[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    """Get all projects (public endpoint)."""
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return projects


@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# ============================================================================
# Project Endpoints - Admin (Requires Authentication)
# ============================================================================

@app.post("/projects", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new project (admin only)."""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing project (admin only)."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a project (admin only)."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"detail": "Project deleted successfully"}


# ============================================================================
# Initialization Endpoint (Run Once After Deployment)
# ============================================================================

@app.post("/init")
def initialize_database(db: Session = Depends(get_db)):
    """
    Initialize database with default admin user.
    This should only be called once after deployment!
    Run via: curl -X POST http://localhost:8000/init
    """
    # Check if admin user already exists
    admin_user = db.query(User).filter(User.username == settings.admin_username).first()
    if admin_user:
        return {"detail": "Admin user already exists"}
    
    # Create admin user
    hashed_password = get_password_hash(settings.admin_password)
    admin_user = User(
        username=settings.admin_username,
        hashed_password=hashed_password,
        is_active=True,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    return {
        "detail": "Admin user created successfully",
        "username": admin_user.username,
        "user_id": admin_user.id,
    }


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
