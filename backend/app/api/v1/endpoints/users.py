"""
Endpoints de usuarios (ejemplo).
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter()


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


# Datos de ejemplo (reemplazar con base de datos real)
fake_users_db = [
    {"id": 1, "email": "user@example.com", "username": "testuser", "is_active": True}
]


@router.get("", response_model=List[UserResponse])
async def list_users():
    """Listar todos los usuarios."""
    return fake_users_db


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Obtener un usuario por ID."""
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """Crear un nuevo usuario."""
    new_user = {
        "id": len(fake_users_db) + 1,
        "email": user.email,
        "username": user.username,
        "is_active": True
    }
    fake_users_db.append(new_user)
    return new_user
