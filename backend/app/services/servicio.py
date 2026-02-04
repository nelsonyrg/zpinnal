"""
Servicio CRUD para la entidad Servicio.
"""
from typing import List, Optional
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.servicio import Servicio
from app.models.categoria import Categoria
from app.schemas.servicio import ServicioCreate, ServicioUpdate


class ServicioService:
    """Servicio para operaciones CRUD de Servicio."""

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        solo_activos: bool = False,
        categoria_id: Optional[int] = None
    ) -> List[Servicio]:
        """Obtener todos los servicios con filtros opcionales."""
        query = select(Servicio).options(selectinload(Servicio.categorias))

        conditions = []
        if solo_activos:
            conditions.append(Servicio.activo == True)
        if categoria_id:
            query = query.join(Servicio.categorias).where(Categoria.id == categoria_id)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.offset(skip).limit(limit).order_by(Servicio.nombre)

        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, servicio_id: int) -> Optional[Servicio]:
        """Obtener un servicio por ID."""
        query = select(Servicio).options(
            selectinload(Servicio.categorias)
        ).where(Servicio.id == servicio_id)

        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_nombre(db: AsyncSession, nombre: str) -> Optional[Servicio]:
        """Obtener un servicio por nombre."""
        query = select(Servicio).where(Servicio.nombre == nombre)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def _load_categorias(db: AsyncSession, categoria_ids: List[int]) -> List[Categoria]:
        """Cargar categorías por sus IDs."""
        if not categoria_ids:
            return []
        query = select(Categoria).where(Categoria.id.in_(categoria_ids))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, servicio_data: ServicioCreate) -> Servicio:
        """Crear un nuevo servicio con categorías asignadas."""
        data = servicio_data.model_dump(exclude={"categoria_ids"})
        servicio = Servicio(**data)

        # Asignar categorías
        if servicio_data.categoria_ids:
            categorias = await ServicioService._load_categorias(db, servicio_data.categoria_ids)
            servicio.categorias = categorias

        db.add(servicio)
        await db.commit()
        await db.refresh(servicio)

        return await ServicioService.get_by_id(db, servicio.id)

    @staticmethod
    async def update(
        db: AsyncSession,
        servicio_id: int,
        servicio_data: ServicioUpdate
    ) -> Optional[Servicio]:
        """Actualizar un servicio existente."""
        servicio = await ServicioService.get_by_id(db, servicio_id)
        if not servicio:
            return None

        update_data = servicio_data.model_dump(exclude_unset=True, exclude={"categoria_ids"})
        for field, value in update_data.items():
            setattr(servicio, field, value)

        # Actualizar categorías si se proporcionan
        if servicio_data.categoria_ids is not None:
            categorias = await ServicioService._load_categorias(db, servicio_data.categoria_ids)
            servicio.categorias = categorias

        await db.commit()
        await db.refresh(servicio)

        return await ServicioService.get_by_id(db, servicio_id)

    @staticmethod
    async def delete(db: AsyncSession, servicio_id: int) -> bool:
        """Eliminar un servicio."""
        servicio = await ServicioService.get_by_id(db, servicio_id)
        if not servicio:
            return False

        await db.delete(servicio)
        await db.commit()
        return True

    @staticmethod
    async def toggle_activo(db: AsyncSession, servicio_id: int) -> Optional[Servicio]:
        """Cambiar el estado activo/inactivo de un servicio."""
        servicio = await ServicioService.get_by_id(db, servicio_id)
        if not servicio:
            return None

        servicio.activo = not servicio.activo
        await db.commit()
        await db.refresh(servicio)

        return await ServicioService.get_by_id(db, servicio_id)

    @staticmethod
    async def count(db: AsyncSession, solo_activos: bool = False) -> int:
        """Contar total de servicios."""
        query = select(func.count(Servicio.id))
        if solo_activos:
            query = query.where(Servicio.activo == True)
        result = await db.execute(query)
        return result.scalar()
