<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCategoriaStore } from '@/stores/categoriaStore'
import type { Categoria } from '@/types/categoria'

const emit = defineEmits<{
  (e: 'editar', categoria: Categoria): void
  (e: 'nueva'): void
}>()

const store = useCategoriaStore()

// Filtros
const filtroActivos = ref<boolean | null>(null)
const filtroRaiz = ref(false)

// Confirmación de eliminación
const categoriaAEliminar = ref<Categoria | null>(null)
const mostrarConfirmacion = ref(false)

// Cargar categorías
async function cargar() {
  await store.cargarCategorias({
    solo_activos: filtroActivos.value === true,
    solo_raiz: filtroRaiz.value
  })
}

// Editar categoría
function editar(categoria: Categoria) {
  emit('editar', categoria)
}

// Nueva categoría
function nueva() {
  emit('nueva')
}

// Toggle activo
async function toggleActivo(categoria: Categoria) {
  await store.toggleActivo(categoria.id)
}

// Confirmar eliminación
function confirmarEliminar(categoria: Categoria) {
  categoriaAEliminar.value = categoria
  mostrarConfirmacion.value = true
}

// Eliminar categoría
async function eliminar() {
  if (categoriaAEliminar.value) {
    try {
      await store.eliminarCategoria(categoriaAEliminar.value.id)
    } catch (error) {
      // El error ya se maneja en el store
    }
  }
  mostrarConfirmacion.value = false
  categoriaAEliminar.value = null
}

// Cancelar eliminación
function cancelarEliminar() {
  mostrarConfirmacion.value = false
  categoriaAEliminar.value = null
}

// Cargar al montar
onMounted(() => {
  cargar()
})
</script>

<template>
  <div class="categoria-lista">
    <!-- Header -->
    <div class="lista-header">
      <h2>Categorías</h2>
      <button class="btn btn-primary" @click="nueva">
        + Nueva Categoría
      </button>
    </div>

    <!-- Filtros -->
    <div class="filtros">
      <label class="filtro-item">
        <select v-model="filtroActivos" @change="cargar">
          <option :value="null">Todos los estados</option>
          <option :value="true">Solo activos</option>
          <option :value="false">Solo inactivos</option>
        </select>
      </label>

      <label class="filtro-item checkbox">
        <input type="checkbox" v-model="filtroRaiz" @change="cargar" />
        <span>Solo categorías raíz</span>
      </label>
    </div>

    <!-- Error -->
    <div v-if="store.error" class="error-message">
      {{ store.error }}
      <button @click="store.limpiarError" class="btn-close">×</button>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="loading">
      Cargando categorías...
    </div>

    <!-- Lista vacía -->
    <div v-else-if="store.categorias.length === 0" class="lista-vacia">
      <p>No hay categorías registradas</p>
      <button class="btn btn-primary" @click="nueva">
        Crear primera categoría
      </button>
    </div>

    <!-- Tabla de categorías -->
    <table v-else class="tabla">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Categoría Padre</th>
          <th>Subcategorías</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="categoria in store.categorias" :key="categoria.id">
          <td>
            <div class="categoria-nombre">
              <img
                v-if="categoria.icono"
                :src="categoria.icono"
                :alt="categoria.nombre"
                class="categoria-icono"
              />
              <span>{{ categoria.nombre }}</span>
            </div>
          </td>
          <td>
            {{ categoria.categoria_padre?.nombre || '—' }}
          </td>
          <td>
            {{ categoria.subcategorias?.length || 0 }}
          </td>
          <td>
            <span
              class="estado-badge"
              :class="categoria.activo ? 'activo' : 'inactivo'"
              @click="toggleActivo(categoria)"
            >
              {{ categoria.activo ? 'Activo' : 'Inactivo' }}
            </span>
          </td>
          <td>
            <div class="acciones">
              <button
                class="btn-accion editar"
                @click="editar(categoria)"
                title="Editar"
              >
                Editar
              </button>
              <button
                class="btn-accion eliminar"
                @click="confirmarEliminar(categoria)"
                title="Eliminar"
                :disabled="(categoria.subcategorias?.length || 0) > 0"
              >
                Eliminar
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal de confirmación -->
    <div v-if="mostrarConfirmacion" class="modal-overlay">
      <div class="modal">
        <h3>Confirmar eliminación</h3>
        <p>
          ¿Está seguro de eliminar la categoría
          <strong>{{ categoriaAEliminar?.nombre }}</strong>?
        </p>
        <p class="warning">Esta acción no se puede deshacer.</p>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="cancelarEliminar">
            Cancelar
          </button>
          <button class="btn btn-danger" @click="eliminar">
            Eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.categoria-lista {
  padding: 1rem;
}

.lista-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.lista-header h2 {
  margin: 0;
}

.filtros {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.filtro-item select {
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}

.filtro-item.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-message {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffebee;
  color: #c62828;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #c62828;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.lista-vacia {
  text-align: center;
  padding: 3rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.lista-vacia p {
  margin-bottom: 1rem;
  color: #666;
}

.tabla {
  width: 100%;
  border-collapse: collapse;
}

.tabla th,
.tabla td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.tabla th {
  background-color: #f5f5f5;
  font-weight: 600;
}

.tabla tr:hover {
  background-color: #fafafa;
}

.categoria-nombre {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.categoria-icono {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.estado-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.estado-badge.activo {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.estado-badge.inactivo {
  background-color: #ffebee;
  color: #c62828;
}

.estado-badge:hover {
  opacity: 0.8;
}

.acciones {
  display: flex;
  gap: 0.5rem;
}

.btn-accion {
  padding: 0.375rem 0.75rem;
  border: none;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-accion.editar {
  background-color: #e3f2fd;
  color: #1565c0;
}

.btn-accion.editar:hover {
  background-color: #bbdefb;
}

.btn-accion.eliminar {
  background-color: #ffebee;
  color: #c62828;
}

.btn-accion.eliminar:hover:not(:disabled) {
  background-color: #ffcdd2;
}

.btn-accion:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background-color: #3aa876;
}

.btn-secondary {
  background-color: #e0e0e0;
  color: #333;
}

.btn-danger {
  background-color: #c62828;
  color: white;
}

.btn-danger:hover {
  background-color: #b71c1c;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
}

.modal h3 {
  margin-top: 0;
}

.modal .warning {
  color: #c62828;
  font-size: 0.9rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
</style>
