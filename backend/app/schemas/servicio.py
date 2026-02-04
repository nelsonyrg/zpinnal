"""
Schemas Pydantic para la entidad Servicio.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.categoria import CategoriaSimple


class ServicioBase(BaseModel):
    """Schema base para Servicio."""
    nombre: str = Field(..., min_length=1, max_length=300, description="Nombre del servicio")
    descripcion: Optional[str] = Field(None, description="Descripción del servicio")
    activo: bool = Field(True, description="Estado activo/inactivo")


class ServicioCreate(ServicioBase):
    """Schema para crear un Servicio."""
    categoria_ids: List[int] = Field(default=[], description="IDs de categorías a asignar")


class ServicioUpdate(BaseModel):
    """Schema para actualizar un Servicio (todos los campos opcionales)."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=300)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None
    categoria_ids: Optional[List[int]] = Field(None, description="IDs de categorías a reasignar")


class ServicioResponse(ServicioBase):
    """Schema de respuesta para Servicio."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    categorias: List[CategoriaSimple] = []
    created_at: datetime
    updated_at: datetime


class ServicioSimple(BaseModel):
    """Schema simplificado de Servicio."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    activo: bool
