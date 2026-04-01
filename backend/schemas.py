from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectCreate(BaseModel):
    """Schema for creating a project."""
    title: str
    description: str
    technologies: str
    github_link: Optional[str] = None
    live_link: Optional[str] = None
    image_url: Optional[str] = None
    featured: bool = False


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    title: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None
    github_link: Optional[str] = None
    live_link: Optional[str] = None
    image_url: Optional[str] = None
    featured: Optional[bool] = None


class ProjectResponse(BaseModel):
    """Schema for returning a project."""
    id: int
    title: str
    description: str
    technologies: str
    github_link: Optional[str] = None
    live_link: Optional[str] = None
    image_url: Optional[str] = None
    featured: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
