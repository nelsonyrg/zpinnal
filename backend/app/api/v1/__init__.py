"""
API v1 Router.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import health, users, categorias

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
