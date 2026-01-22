"""
Endpoints de salud y estado del servicio.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health():
    """Verificar estado del servicio."""
    return {"status": "ok"}


@router.get("/ready")
async def readiness():
    """Verificar si el servicio está listo para recibir tráfico."""
    return {"ready": True}
