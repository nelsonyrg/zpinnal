"""
Modelo SQLAlchemy para la entidad Servicio con relación N:N a Categoría.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

# Tabla intermedia para relación muchos a muchos Servicio <-> Categoria
servicio_categorias = Table(
    "servicio_categorias",
    Base.metadata,
    Column("servicio_id", Integer, ForeignKey("servicios.id", ondelete="CASCADE"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey("categorias.id", ondelete="CASCADE"), primary_key=True),
)


class Servicio(Base):
    """Modelo de Servicio con relación N:N a Categorías."""

    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(300), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relación N:N con Categorías
    categorias = relationship(
        "Categoria",
        secondary=servicio_categorias,
        backref="servicios",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Servicio(id={self.id}, nombre='{self.nombre}')>"
