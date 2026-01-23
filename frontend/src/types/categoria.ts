/**
 * Tipos TypeScript para la entidad Categoria.
 */

export interface CategoriaSimple {
  id: number
  nombre: string
  icono: string | null
  activo: boolean
}

export interface Categoria {
  id: number
  nombre: string
  descripcion: string | null
  icono: string | null
  activo: boolean
  categoria_padre_id: number | null
  categoria_padre: CategoriaSimple | null
  subcategorias: CategoriaSimple[]
  created_at: string
  updated_at: string
}

export interface CategoriaCreate {
  nombre: string
  descripcion?: string | null
  icono?: string | null
  activo?: boolean
  categoria_padre_id?: number | null
}

export interface CategoriaUpdate {
  nombre?: string
  descripcion?: string | null
  icono?: string | null
  activo?: boolean
  categoria_padre_id?: number | null
}

export interface CategoriaTree extends CategoriaSimple {
  descripcion: string | null
  subcategorias: CategoriaTree[]
}

export interface CategoriaFilters {
  skip?: number
  limit?: number
  solo_activos?: boolean
  solo_raiz?: boolean
}
