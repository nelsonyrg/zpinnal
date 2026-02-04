/**
 * Store Pinia para la entidad Servicio.
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { servicioApi } from '@/services/servicioApi'
import type {
  Servicio,
  ServicioCreate,
  ServicioUpdate,
  ServicioFilters
} from '@/types/servicio'

export const useServicioStore = defineStore('servicio', () => {
  // Estado
  const servicios = ref<Servicio[]>([])
  const servicioActual = ref<Servicio | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const totalServicios = ref(0)

  // Getters
  const serviciosActivos = computed(() =>
    servicios.value.filter(s => s.activo)
  )

  // Acciones
  async function cargarServicios(filters: ServicioFilters = {}) {
    loading.value = true
    error.value = null
    try {
      servicios.value = await servicioApi.listar(filters)
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cargar servicios'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function cargarConteo(soloActivos: boolean = false) {
    try {
      totalServicios.value = await servicioApi.contar(soloActivos)
    } catch (e: any) {
      console.error('Error al cargar conteo:', e)
    }
  }

  async function obtenerServicio(id: number) {
    loading.value = true
    error.value = null
    try {
      servicioActual.value = await servicioApi.obtener(id)
      return servicioActual.value
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al obtener servicio'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function crearServicio(data: ServicioCreate) {
    loading.value = true
    error.value = null
    try {
      const nuevo = await servicioApi.crear(data)
      servicios.value.push(nuevo)
      return nuevo
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al crear servicio'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function actualizarServicio(id: number, data: ServicioUpdate) {
    loading.value = true
    error.value = null
    try {
      const actualizado = await servicioApi.actualizar(id, data)
      const index = servicios.value.findIndex(s => s.id === id)
      if (index !== -1) {
        servicios.value[index] = actualizado
      }
      if (servicioActual.value?.id === id) {
        servicioActual.value = actualizado
      }
      return actualizado
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al actualizar servicio'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function toggleActivo(id: number) {
    loading.value = true
    error.value = null
    try {
      const actualizado = await servicioApi.toggleActivo(id)
      const index = servicios.value.findIndex(s => s.id === id)
      if (index !== -1) {
        servicios.value[index] = actualizado
      }
      return actualizado
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cambiar estado'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function eliminarServicio(id: number) {
    loading.value = true
    error.value = null
    try {
      await servicioApi.eliminar(id)
      servicios.value = servicios.value.filter(s => s.id !== id)
      if (servicioActual.value?.id === id) {
        servicioActual.value = null
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al eliminar servicio'
      throw e
    } finally {
      loading.value = false
    }
  }

  function limpiarError() {
    error.value = null
  }

  return {
    servicios,
    servicioActual,
    loading,
    error,
    totalServicios,
    serviciosActivos,
    cargarServicios,
    cargarConteo,
    obtenerServicio,
    crearServicio,
    actualizarServicio,
    toggleActivo,
    eliminarServicio,
    limpiarError
  }
})
