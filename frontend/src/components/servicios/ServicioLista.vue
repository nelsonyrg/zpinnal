<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useServicioStore } from '@/stores/servicioStore'
import { useCategoriaStore } from '@/stores/categoriaStore'
import type { Servicio } from '@/types/servicio'

const emit = defineEmits<{
  (e: 'editar', servicio: Servicio): void
  (e: 'nuevo'): void
}>()

const servicioStore = useServicioStore()
const categoriaStore = useCategoriaStore()

// Filtros
const filtroActivos = ref<boolean | null>(null)
const filtroCategoriaId = ref<number | null>(null)

// Confirmación de eliminación
const servicioAEliminar = ref<Servicio | null>(null)
const mostrarConfirmacion = ref(false)

async function cargar() {
  await servicioStore.cargarServicios({
    solo_activos: filtroActivos.value === true,
    categoria_id: filtroCategoriaId.value || undefined
  })
}

function editar(servicio: Servicio) {
  emit('editar', servicio)
}

function nuevo() {
  emit('nuevo')
}

async function toggleActivo(servicio: Servicio) {
  await servicioStore.toggleActivo(servicio.id)
}

function confirmarEliminar(servicio: Servicio) {
  servicioAEliminar.value = servicio
  mostrarConfirmacion.value = true
}

async function eliminar() {
  if (servicioAEliminar.value) {
    try {
      await servicioStore.eliminarServicio(servicioAEliminar.value.id)
    } catch (error) {
      // Error manejado en el store
    }
  }
  mostrarConfirmacion.value = false
  servicioAEliminar.value = null
}

function cancelarEliminar() {
  mostrarConfirmacion.value = false
  servicioAEliminar.value = null
}

onMounted(async () => {
  await cargar()
  if (categoriaStore.categorias.length === 0) {
    await categoriaStore.cargarCategorias()
  }
})
</script>

<template>
  <div class="servicio-lista">
    <!-- Header -->
    <div class="lista-header">
      <h2>Servicios</h2>
      <button class="btn btn-primary" @click="nuevo">
        + Nuevo Servicio
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

      <label class="filtro-item">
        <select v-model="filtroCategoriaId" @change="cargar">
          <option :value="null">Todas las categorías</option>
          <option
            v-for="cat in categoriaStore.categorias"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.nombre }}
          </option>
        </select>
      </label>
    </div>

    <!-- Error -->
    <div v-if="servicioStore.error" class="error-message">
      {{ servicioStore.error }}
      <button @click="servicioStore.limpiarError" class="btn-close">&times;</button>
    </div>

    <!-- Loading -->
    <div v-if="servicioStore.loading" class="loading">
      Cargando servicios...
    </div>

    <!-- Lista vacía -->
    <div v-else-if="servicioStore.servicios.length === 0" class="lista-vacia">
      <p>No hay servicios registrados</p>
      <button class="btn btn-primary" @click="nuevo">
        Crear primer servicio
      </button>
    </div>

    <!-- Tabla -->
    <table v-else class="tabla">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Categorías</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="servicio in servicioStore.servicios" :key="servicio.id">
          <td>
            <div class="servicio-info">
              <strong>{{ servicio.nombre }}</strong>
              <small v-if="servicio.descripcion" class="descripcion-preview">
                {{ servicio.descripcion.substring(0, 80) }}{{ servicio.descripcion.length > 80 ? '...' : '' }}
              </small>
            </div>
          </td>
          <td>
            <div class="categorias-tags">
              <span
                v-for="cat in servicio.categorias"
                :key="cat.id"
                class="tag"
              >
                {{ cat.nombre }}
              </span>
              <span v-if="servicio.categorias.length === 0" class="sin-categorias">
                Sin categorías
              </span>
            </div>
          </td>
          <td>
            <span
              class="estado-badge"
              :class="servicio.activo ? 'activo' : 'inactivo'"
              @click="toggleActivo(servicio)"
            >
              {{ servicio.activo ? 'Activo' : 'Inactivo' }}
            </span>
          </td>
          <td>
            <div class="acciones">
              <button class="btn-accion editar" @click="editar(servicio)">
                Editar
              </button>
              <button class="btn-accion eliminar" @click="confirmarEliminar(servicio)">
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
          ¿Está seguro de eliminar el servicio
          <strong>{{ servicioAEliminar?.nombre }}</strong>?
        </p>
        <p class="warning">Esta acción no se puede deshacer.</p>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="cancelarEliminar">Cancelar</button>
          <button class="btn btn-danger" @click="eliminar">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.servicio-lista {
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

.servicio-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.descripcion-preview {
  color: #666;
  font-size: 0.85rem;
}

.categorias-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.tag {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  background-color: #e3f2fd;
  color: #1565c0;
  border-radius: 12px;
  font-size: 0.8rem;
}

.sin-categorias {
  color: #999;
  font-size: 0.85rem;
  font-style: italic;
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

.btn-accion.eliminar:hover {
  background-color: #ffcdd2;
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
