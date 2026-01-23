"""
Servicio CRUD para la entidad Categoria.
"""
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


class CategoriaService:
    """Servicio para operaciones CRUD de Categoria."""

    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        solo_activos: bool = False,
        solo_raiz: bool = False
    ) -> List[Categoria]:
        """Obtener todas las categorías con filtros opcionales."""
        query = select(Categoria).options(
            selectinload(Categoria.categoria_padre),
            selectinload(Categoria.subcategorias)
        )

        conditions = []
        if solo_activos:
            conditions.append(Categoria.activo == True)
        if solo_raiz:
            conditions.append(Categoria.categoria_padre_id == None)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.offset(skip).limit(limit).order_by(Categoria.nombre)

        result = await db.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, categoria_id: int) -> Optional[Categoria]:
        """Obtener una categoría por ID."""
        query = select(Categoria).options(
            selectinload(Categoria.categoria_padre),
            selectinload(Categoria.subcategorias)
        ).where(Categoria.id == categoria_id)

        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_nombre(db: AsyncSession, nombre: str) -> Optional[Categoria]:
        """Obtener una categoría por nombre."""
        query = select(Categoria).where(Categoria.nombre == nombre)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_subcategorias(db: AsyncSession, categoria_id: int) -> List[Categoria]:
        """Obtener subcategorías de una categoría."""
        query = select(Categoria).where(
            Categoria.categoria_padre_id == categoria_id
        ).order_by(Categoria.nombre)

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, categoria_data: CategoriaCreate) -> Categoria:
        """Crear una nueva categoría."""
        categoria = Categoria(**categoria_data.model_dump())
        db.add(categoria)
        await db.commit()
        await db.refresh(categoria)

        # Recargar con relaciones
        return await CategoriaService.get_by_id(db, categoria.id)

    @staticmethod
    async def update(
        db: AsyncSession,
        categoria_id: int,
        categoria_data: CategoriaUpdate
    ) -> Optional[Categoria]:
        """Actualizar una categoría existente."""
        categoria = await CategoriaService.get_by_id(db, categoria_id)
        if not categoria:
            return None

        # Actualizar solo campos proporcionados
        update_data = categoria_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(categoria, field, value)

        await db.commit()
        await db.refresh(categoria)

        return await CategoriaService.get_by_id(db, categoria_id)

    @staticmethod
    async def delete(db: AsyncSession, categoria_id: int) -> bool:
        """Eliminar una categoría."""
        categoria = await CategoriaService.get_by_id(db, categoria_id)
        if not categoria:
            return False

        await db.delete(categoria)
        await db.commit()
        return True

    @staticmethod
    async def toggle_activo(db: AsyncSession, categoria_id: int) -> Optional[Categoria]:
        """Cambiar el estado activo/inactivo de una categoría."""
        categoria = await CategoriaService.get_by_id(db, categoria_id)
        if not categoria:
            return None

        categoria.activo = not categoria.activo
        await db.commit()
        await db.refresh(categoria)

        return categoria

    @staticmethod
    async def get_tree(db: AsyncSession, solo_activos: bool = True) -> List[Categoria]:
        """Obtener árbol de categorías (solo raíz con subcategorías cargadas)."""
        return await CategoriaService.get_all(
            db,
            solo_activos=solo_activos,
            solo_raiz=True,
            limit=1000
        )

    @staticmethod
    async def count(db: AsyncSession, solo_activos: bool = False) -> int:
        """Contar total de categorías."""
        from sqlalchemy import func
        query = select(func.count(Categoria.id))
        if solo_activos:
            query = query.where(Categoria.activo == True)
        result = await db.execute(query)
        return result.scalar()
