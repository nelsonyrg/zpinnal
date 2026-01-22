"""
FastAPI Backend - Punto de entrada principal
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import router as api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación."""
    # Startup
    print("🚀 Iniciando aplicación...")
    yield
    # Shutdown
    print("👋 Cerrando aplicación...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Backend para aplicación móvil Vue.js/Capacitor",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar estado del servicio."""
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "message": "API Backend activo",
        "docs": "/docs",
        "health": "/health"
    }
