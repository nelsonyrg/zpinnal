"""
Modelo SQLAlchemy para la entidad Categoria.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Categoria(Base):
    """Modelo de Categoria con relación autoreferencial para categoria padre."""

    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, index=True)
    descripcion = Column(Text(1000), nullable=True)
    icono = Column(String(700), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    # Relación autoreferencial - categoria padre (opcional)
    categoria_padre_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    categoria_padre = relationship(
        "Categoria",
        remote_side=[id],
        backref="subcategorias",
        lazy="joined"
    )

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"
