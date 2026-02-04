/**
 * Tipos TypeScript para la entidad Servicio.
 */
import type { CategoriaSimple } from './categoria'

export interface Servicio {
  id: number
  nombre: string
  descripcion: string | null
  activo: boolean
  categorias: CategoriaSimple[]
  created_at: string
  updated_at: string
}

export interface ServicioCreate {
  nombre: string
  descripcion?: string | null
  activo?: boolean
  categoria_ids: number[]
}

export interface ServicioUpdate {
  nombre?: string
  descripcion?: string | null
  activo?: boolean
  categoria_ids?: number[]
}

export interface ServicioSimple {
  id: number
  nombre: string
  activo: boolean
}

export interface ServicioFilters {
  skip?: number
  limit?: number
  solo_activos?: boolean
  categoria_id?: number | null
}
