"""
Endpoints API para la entidad Servicio.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.servicio import ServicioService
from app.services.categoria import CategoriaService
from app.schemas.servicio import (
    ServicioCreate,
    ServicioUpdate,
    ServicioResponse,
)

router = APIRouter()


@router.get("", response_model=List[ServicioResponse])
async def listar_servicios(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros"),
    solo_activos: bool = Query(False, description="Filtrar solo activos"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    db: AsyncSession = Depends(get_db),
):
    """Listar todos los servicios con filtros opcionales."""
    servicios = await ServicioService.get_all(
        db,
        skip=skip,
        limit=limit,
        solo_activos=solo_activos,
        categoria_id=categoria_id
    )
    return servicios


@router.get("/count")
async def contar_servicios(
    solo_activos: bool = Query(False, description="Contar solo activos"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener conteo total de servicios."""
    total = await ServicioService.count(db, solo_activos=solo_activos)
    return {"total": total}


@router.get("/{servicio_id}", response_model=ServicioResponse)
async def obtener_servicio(
    servicio_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Obtener un servicio por ID."""
    servicio = await ServicioService.get_by_id(db, servicio_id)
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {servicio_id} no encontrado"
        )
    return servicio


@router.post("", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
async def crear_servicio(
    servicio_data: ServicioCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crear un nuevo servicio."""
    # Verificar nombre único
    existente = await ServicioService.get_by_nombre(db, servicio_data.nombre)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un servicio con el nombre '{servicio_data.nombre}'"
        )

    # Verificar que las categorías existen
    for cat_id in servicio_data.categoria_ids:
        cat = await CategoriaService.get_by_id(db, cat_id)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría con ID {cat_id} no encontrada"
            )

    servicio = await ServicioService.create(db, servicio_data)
    return servicio


@router.put("/{servicio_id}", response_model=ServicioResponse)
async def actualizar_servicio(
    servicio_id: int,
    servicio_data: ServicioUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Actualizar un servicio existente."""
    servicio = await ServicioService.get_by_id(db, servicio_id)
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {servicio_id} no encontrado"
        )

    # Verificar nombre único si se actualiza
    if servicio_data.nombre and servicio_data.nombre != servicio.nombre:
        existente = await ServicioService.get_by_nombre(db, servicio_data.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un servicio con el nombre '{servicio_data.nombre}'"
            )

    # Verificar categorías si se proporcionan
    if servicio_data.categoria_ids is not None:
        for cat_id in servicio_data.categoria_ids:
            cat = await CategoriaService.get_by_id(db, cat_id)
            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Categoría con ID {cat_id} no encontrada"
                )

    servicio_actualizado = await ServicioService.update(db, servicio_id, servicio_data)
    return servicio_actualizado


@router.patch("/{servicio_id}/toggle-activo", response_model=ServicioResponse)
async def toggle_activo_servicio(
    servicio_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Cambiar estado activo/inactivo de un servicio."""
    servicio = await ServicioService.toggle_activo(db, servicio_id)
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {servicio_id} no encontrado"
        )
    return servicio


@router.delete("/{servicio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_servicio(
    servicio_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Eliminar un servicio."""
    eliminado = await ServicioService.delete(db, servicio_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {servicio_id} no encontrado"
        )
    return None
