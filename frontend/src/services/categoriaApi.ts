/**
 * Servicio API para la entidad Categoria.
 */
import apiClient from './api'
import type {
  Categoria,
  CategoriaCreate,
  CategoriaUpdate,
  CategoriaTree,
  CategoriaFilters
} from '@/types/categoria'

const BASE_URL = '/categorias'

export const categoriaApi = {
  /**
   * Listar todas las categorías con filtros opcionales.
   */
  async listar(filters: CategoriaFilters = {}): Promise<Categoria[]> {
    const params = new URLSearchParams()

    if (filters.skip !== undefined) params.append('skip', filters.skip.toString())
    if (filters.limit !== undefined) params.append('limit', filters.limit.toString())
    if (filters.solo_activos !== undefined) params.append('solo_activos', filters.solo_activos.toString())
    if (filters.solo_raiz !== undefined) params.append('solo_raiz', filters.solo_raiz.toString())

    const response = await apiClient.get(`${BASE_URL}?${params.toString()}`)
    return response.data
  },

  /**
   * Obtener árbol jerárquico de categorías.
   */
  async obtenerArbol(soloActivos: boolean = true): Promise<CategoriaTree[]> {
    const response = await apiClient.get(`${BASE_URL}/tree?solo_activos=${soloActivos}`)
    return response.data
  },

  /**
   * Obtener conteo total de categorías.
   */
  async contar(soloActivos: boolean = false): Promise<number> {
    const response = await apiClient.get(`${BASE_URL}/count?solo_activos=${soloActivos}`)
    return response.data.total
  },

  /**
   * Obtener una categoría por ID.
   */
  async obtener(id: number): Promise<Categoria> {
    const response = await apiClient.get(`${BASE_URL}/${id}`)
    return response.data
  },

  /**
   * Obtener subcategorías de una categoría.
   */
  async obtenerSubcategorias(id: number): Promise<Categoria[]> {
    const response = await apiClient.get(`${BASE_URL}/${id}/subcategorias`)
    return response.data
  },

  /**
   * Crear una nueva categoría.
   */
  async crear(data: CategoriaCreate): Promise<Categoria> {
    const response = await apiClient.post(BASE_URL, data)
    return response.data
  },

  /**
   * Actualizar una categoría existente.
   */
  async actualizar(id: number, data: CategoriaUpdate): Promise<Categoria> {
    const response = await apiClient.put(`${BASE_URL}/${id}`, data)
    return response.data
  },

  /**
   * Cambiar estado activo/inactivo de una categoría.
   */
  async toggleActivo(id: number): Promise<Categoria> {
    const response = await apiClient.patch(`${BASE_URL}/${id}/toggle-activo`)
    return response.data
  },

  /**
   * Eliminar una categoría.
   */
  async eliminar(id: number): Promise<void> {
    await apiClient.delete(`${BASE_URL}/${id}`)
  }
}

export default categoriaApi
