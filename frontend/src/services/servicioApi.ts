/**
 * Servicio API para la entidad Servicio.
 */
import apiClient from './api'
import type {
  Servicio,
  ServicioCreate,
  ServicioUpdate,
  ServicioFilters
} from '@/types/servicio'

const BASE_URL = '/servicios'

export const servicioApi = {
  async listar(filters: ServicioFilters = {}): Promise<Servicio[]> {
    const params = new URLSearchParams()
    if (filters.skip !== undefined) params.append('skip', filters.skip.toString())
    if (filters.limit !== undefined) params.append('limit', filters.limit.toString())
    if (filters.solo_activos !== undefined) params.append('solo_activos', filters.solo_activos.toString())
    if (filters.categoria_id) params.append('categoria_id', filters.categoria_id.toString())

    const response = await apiClient.get(`${BASE_URL}?${params.toString()}`)
    return response.data
  },

  async contar(soloActivos: boolean = false): Promise<number> {
    const response = await apiClient.get(`${BASE_URL}/count?solo_activos=${soloActivos}`)
    return response.data.total
  },

  async obtener(id: number): Promise<Servicio> {
    const response = await apiClient.get(`${BASE_URL}/${id}`)
    return response.data
  },

  async crear(data: ServicioCreate): Promise<Servicio> {
    const response = await apiClient.post(BASE_URL, data)
    return response.data
  },

  async actualizar(id: number, data: ServicioUpdate): Promise<Servicio> {
    const response = await apiClient.put(`${BASE_URL}/${id}`, data)
    return response.data
  },

  async toggleActivo(id: number): Promise<Servicio> {
    const response = await apiClient.patch(`${BASE_URL}/${id}/toggle-activo`)
    return response.data
  },

  async eliminar(id: number): Promise<void> {
    await apiClient.delete(`${BASE_URL}/${id}`)
  }
}

export default servicioApi
