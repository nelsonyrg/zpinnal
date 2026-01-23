/**
 * Store Pinia para la entidad Categoria.
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { categoriaApi } from '@/services/categoriaApi'
import type {
  Categoria,
  CategoriaCreate,
  CategoriaUpdate,
  CategoriaTree,
  CategoriaFilters
} from '@/types/categoria'

export const useCategoriaStore = defineStore('categoria', () => {
  // Estado
  const categorias = ref<Categoria[]>([])
  const categoriaActual = ref<Categoria | null>(null)
  const arbolCategorias = ref<CategoriaTree[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const totalCategorias = ref(0)

  // Getters
  const categoriasActivas = computed(() =>
    categorias.value.filter(c => c.activo)
  )

  const categoriasRaiz = computed(() =>
    categorias.value.filter(c => c.categoria_padre_id === null)
  )

  const categoriasParaSelector = computed(() =>
    categorias.value.map(c => ({
      value: c.id,
      label: c.nombre,
      disabled: !c.activo
    }))
  )

  // Acciones
  async function cargarCategorias(filters: CategoriaFilters = {}) {
    loading.value = true
    error.value = null
    try {
      categorias.value = await categoriaApi.listar(filters)
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cargar categorías'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function cargarArbol(soloActivos: boolean = true) {
    loading.value = true
    error.value = null
    try {
      arbolCategorias.value = await categoriaApi.obtenerArbol(soloActivos)
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cargar árbol de categorías'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function cargarConteo(soloActivos: boolean = false) {
    try {
      totalCategorias.value = await categoriaApi.contar(soloActivos)
    } catch (e: any) {
      console.error('Error al cargar conteo:', e)
    }
  }

  async function obtenerCategoria(id: number) {
    loading.value = true
    error.value = null
    try {
      categoriaActual.value = await categoriaApi.obtener(id)
      return categoriaActual.value
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al obtener categoría'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function crearCategoria(data: CategoriaCreate) {
    loading.value = true
    error.value = null
    try {
      const nueva = await categoriaApi.crear(data)
      categorias.value.push(nueva)
      return nueva
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al crear categoría'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function actualizarCategoria(id: number, data: CategoriaUpdate) {
    loading.value = true
    error.value = null
    try {
      const actualizada = await categoriaApi.actualizar(id, data)
      const index = categorias.value.findIndex(c => c.id === id)
      if (index !== -1) {
        categorias.value[index] = actualizada
      }
      if (categoriaActual.value?.id === id) {
        categoriaActual.value = actualizada
      }
      return actualizada
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al actualizar categoría'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function toggleActivo(id: number) {
    loading.value = true
    error.value = null
    try {
      const actualizada = await categoriaApi.toggleActivo(id)
      const index = categorias.value.findIndex(c => c.id === id)
      if (index !== -1) {
        categorias.value[index] = actualizada
      }
      return actualizada
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al cambiar estado'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function eliminarCategoria(id: number) {
    loading.value = true
    error.value = null
    try {
      await categoriaApi.eliminar(id)
      categorias.value = categorias.value.filter(c => c.id !== id)
      if (categoriaActual.value?.id === id) {
        categoriaActual.value = null
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Error al eliminar categoría'
      throw e
    } finally {
      loading.value = false
    }
  }

  function limpiarError() {
    error.value = null
  }

  function limpiarCategoriaActual() {
    categoriaActual.value = null
  }

  return {
    // Estado
    categorias,
    categoriaActual,
    arbolCategorias,
    loading,
    error,
    totalCategorias,

    // Getters
    categoriasActivas,
    categoriasRaiz,
    categoriasParaSelector,

    // Acciones
    cargarCategorias,
    cargarArbol,
    cargarConteo,
    obtenerCategoria,
    crearCategoria,
    actualizarCategoria,
    toggleActivo,
    eliminarCategoria,
    limpiarError,
    limpiarCategoriaActual
  }
})
