"""
Schemas Pydantic para la entidad Categoria.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CategoriaBase(BaseModel):
    """Schema base para Categoria."""
    nombre: str = Field(..., min_length=1, max_length=150, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, max_length=1000, description="Descripción de la categoría")
    icono: Optional[str] = Field(None, max_length=700, description="Ruta del icono")
    activo: bool = Field(True, description="Estado activo/inactivo")
    categoria_padre_id: Optional[int] = Field(None, description="ID de la categoría padre")


class CategoriaCreate(CategoriaBase):
    """Schema para crear una Categoria."""
    pass


class CategoriaUpdate(BaseModel):
    """Schema para actualizar una Categoria (todos los campos opcionales)."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    descripcion: Optional[str] = Field(None, max_length=1000)
    icono: Optional[str] = Field(None, max_length=700)
    activo: Optional[bool] = None
    categoria_padre_id: Optional[int] = None


class CategoriaInDB(CategoriaBase):
    """Schema para Categoria en base de datos."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class CategoriaResponse(CategoriaInDB):
    """Schema de respuesta para Categoria."""
    categoria_padre: Optional["CategoriaSimple"] = None
    subcategorias: Optional[List["CategoriaSimple"]] = []


class CategoriaSimple(BaseModel):
    """Schema simplificado para evitar recursión infinita."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    icono: Optional[str] = None
    activo: bool


class CategoriaTree(CategoriaSimple):
    """Schema para árbol de categorías."""
    model_config = ConfigDict(from_attributes=True)

    descripcion: Optional[str] = None
    subcategorias: List["CategoriaTree"] = []


# Actualizar referencias forward
CategoriaResponse.model_rebuild()
CategoriaTree.model_rebuild()
