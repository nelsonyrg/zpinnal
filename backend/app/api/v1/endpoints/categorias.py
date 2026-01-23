"""
Endpoints API para la entidad Categoria.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.categoria import CategoriaService
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
    CategoriaTree,
)

router = APIRouter()


@router.get("", response_model=List[CategoriaResponse])
async def listar_categorias(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros"),
    solo_activos: bool = Query(False, description="Filtrar solo activos"),
    solo_raiz: bool = Query(False, description="Filtrar solo categorías raíz"),
    db: AsyncSession = Depends(get_db),
):
    """Listar todas las categorías con filtros opcionales."""
    categorias = await CategoriaService.get_all(
        db,
        skip=skip,
        limit=limit,
        solo_activos=solo_activos,
        solo_raiz=solo_raiz
    )
    return categorias


@router.get("/tree", response_model=List[CategoriaTree])
async def obtener_arbol_categorias(
    solo_activos: bool = Query(True, description="Filtrar solo activos"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener árbol jerárquico de categorías."""
    categorias = await CategoriaService.get_tree(db, solo_activos=solo_activos)
    return categorias


@router.get("/count")
async def contar_categorias(
    solo_activos: bool = Query(False, description="Contar solo activos"),
    db: AsyncSession = Depends(get_db),
):
    """Obtener conteo total de categorías."""
    total = await CategoriaService.count(db, solo_activos=solo_activos)
    return {"total": total}


@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def obtener_categoria(
    categoria_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Obtener una categoría por ID."""
    categoria = await CategoriaService.get_by_id(db, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria


@router.get("/{categoria_id}/subcategorias", response_model=List[CategoriaResponse])
async def obtener_subcategorias(
    categoria_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Obtener subcategorías de una categoría."""
    # Verificar que la categoría padre existe
    categoria = await CategoriaService.get_by_id(db, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )

    subcategorias = await CategoriaService.get_subcategorias(db, categoria_id)
    return subcategorias


@router.post("", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    categoria_data: CategoriaCreate,
    db: AsyncSession = Depends(get_db),
):
    """Crear una nueva categoría."""
    # Verificar si el nombre ya existe
    existente = await CategoriaService.get_by_nombre(db, categoria_data.nombre)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una categoría con el nombre '{categoria_data.nombre}'"
        )

    # Verificar que la categoría padre existe si se proporciona
    if categoria_data.categoria_padre_id:
        padre = await CategoriaService.get_by_id(db, categoria_data.categoria_padre_id)
        if not padre:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría padre con ID {categoria_data.categoria_padre_id} no encontrada"
            )

    categoria = await CategoriaService.create(db, categoria_data)
    return categoria


@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def actualizar_categoria(
    categoria_id: int,
    categoria_data: CategoriaUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Actualizar una categoría existente."""
    # Verificar que la categoría existe
    categoria = await CategoriaService.get_by_id(db, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )

    # Verificar nombre único si se está actualizando
    if categoria_data.nombre and categoria_data.nombre != categoria.nombre:
        existente = await CategoriaService.get_by_nombre(db, categoria_data.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una categoría con el nombre '{categoria_data.nombre}'"
            )

    # Verificar categoría padre si se proporciona
    if categoria_data.categoria_padre_id:
        # No puede ser su propio padre
        if categoria_data.categoria_padre_id == categoria_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Una categoría no puede ser su propia categoría padre"
            )
        padre = await CategoriaService.get_by_id(db, categoria_data.categoria_padre_id)
        if not padre:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría padre con ID {categoria_data.categoria_padre_id} no encontrada"
            )

    categoria_actualizada = await CategoriaService.update(db, categoria_id, categoria_data)
    return categoria_actualizada


@router.patch("/{categoria_id}/toggle-activo", response_model=CategoriaResponse)
async def toggle_activo_categoria(
    categoria_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Cambiar estado activo/inactivo de una categoría."""
    categoria = await CategoriaService.toggle_activo(db, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_categoria(
    categoria_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Eliminar una categoría."""
    # Verificar que no tenga subcategorías
    subcategorias = await CategoriaService.get_subcategorias(db, categoria_id)
    if subcategorias:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una categoría que tiene subcategorías"
        )

    eliminado = await CategoriaService.delete(db, categoria_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría con ID {categoria_id} no encontrada"
        )
    return None
