<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useServicioStore } from '@/stores/servicioStore'
import { useCategoriaStore } from '@/stores/categoriaStore'
import type { Servicio, ServicioCreate, ServicioUpdate } from '@/types/servicio'

const props = defineProps<{
  servicio?: Servicio | null
  modo: 'crear' | 'editar'
}>()

const emit = defineEmits<{
  (e: 'guardado', servicio: Servicio): void
  (e: 'cancelado'): void
}>()

const servicioStore = useServicioStore()
const categoriaStore = useCategoriaStore()

// Estado del formulario
const form = ref({
  nombre: '',
  descripcion: '',
  activo: true,
  categoria_ids: [] as number[]
})

const errores = ref<Record<string, string>>({})
const guardando = ref(false)

const titulo = computed(() =>
  props.modo === 'crear' ? 'Nuevo Servicio' : 'Editar Servicio'
)

// Cargar datos si es edición
watch(() => props.servicio, (nuevoServicio) => {
  if (nuevoServicio && props.modo === 'editar') {
    form.value = {
      nombre: nuevoServicio.nombre,
      descripcion: nuevoServicio.descripcion || '',
      activo: nuevoServicio.activo,
      categoria_ids: nuevoServicio.categorias.map(c => c.id)
    }
  }
}, { immediate: true })

// Toggle de categoría
function toggleCategoria(catId: number) {
  const index = form.value.categoria_ids.indexOf(catId)
  if (index === -1) {
    form.value.categoria_ids.push(catId)
  } else {
    form.value.categoria_ids.splice(index, 1)
  }
}

function estaSeleccionada(catId: number): boolean {
  return form.value.categoria_ids.includes(catId)
}

// Validación
function validar(): boolean {
  errores.value = {}

  if (!form.value.nombre.trim()) {
    errores.value.nombre = 'El nombre es requerido'
  } else if (form.value.nombre.length > 300) {
    errores.value.nombre = 'El nombre no puede exceder 300 caracteres'
  }

  return Object.keys(errores.value).length === 0
}

// Guardar
async function guardar() {
  if (!validar()) return

  guardando.value = true
  try {
    let resultado: Servicio

    if (props.modo === 'crear') {
      const createData: ServicioCreate = {
        nombre: form.value.nombre,
        descripcion: form.value.descripcion || null,
        activo: form.value.activo,
        categoria_ids: form.value.categoria_ids
      }
      resultado = await servicioStore.crearServicio(createData)
    } else {
      const updateData: ServicioUpdate = {
        nombre: form.value.nombre,
        descripcion: form.value.descripcion || null,
        activo: form.value.activo,
        categoria_ids: form.value.categoria_ids
      }
      resultado = await servicioStore.actualizarServicio(props.servicio!.id, updateData)
    }

    emit('guardado', resultado)
  } catch (error: any) {
    if (error.response?.data?.detail) {
      errores.value.general = error.response.data.detail
    }
  } finally {
    guardando.value = false
  }
}

function cancelar() {
  emit('cancelado')
}

// Cargar categorías para el selector
onMounted(async () => {
  if (categoriaStore.categorias.length === 0) {
    await categoriaStore.cargarCategorias({ solo_activos: true })
  }
})
</script>

<template>
  <div class="servicio-form">
    <h2>{{ titulo }}</h2>

    <form @submit.prevent="guardar">
      <!-- Error general -->
      <div v-if="errores.general" class="error-message">
        {{ errores.general }}
      </div>

      <!-- Nombre -->
      <div class="form-group">
        <label for="nombre" class="form-label">Nombre *</label>
        <input
          id="nombre"
          v-model="form.nombre"
          type="text"
          class="form-input"
          :class="{ 'input-error': errores.nombre }"
          maxlength="300"
          placeholder="Nombre del servicio"
        />
        <span v-if="errores.nombre" class="field-error">{{ errores.nombre }}</span>
        <span class="char-count">{{ form.nombre.length }}/300</span>
      </div>

      <!-- Descripción -->
      <div class="form-group">
        <label for="descripcion" class="form-label">Descripción</label>
        <textarea
          id="descripcion"
          v-model="form.descripcion"
          class="form-input"
          rows="5"
          placeholder="Descripción del servicio"
        ></textarea>
      </div>

      <!-- Categorías (selector múltiple) -->
      <div class="form-group">
        <label class="form-label">
          Categorías
          <span class="badge">{{ form.categoria_ids.length }} seleccionadas</span>
        </label>
        <div class="categorias-selector">
          <div v-if="categoriaStore.loading" class="loading-small">
            Cargando categorías...
          </div>
          <div v-else-if="categoriaStore.categorias.length === 0" class="empty-small">
            No hay categorías disponibles
          </div>
          <div
            v-for="cat in categoriaStore.categorias"
            :key="cat.id"
            class="categoria-chip"
            :class="{ selected: estaSeleccionada(cat.id) }"
            @click="toggleCategoria(cat.id)"
          >
            <img
              v-if="cat.icono"
              :src="cat.icono"
              :alt="cat.nombre"
              class="chip-icono"
            />
            <span>{{ cat.nombre }}</span>
            <span v-if="estaSeleccionada(cat.id)" class="chip-check">&#10003;</span>
          </div>
        </div>
      </div>

      <!-- Activo -->
      <div class="form-group checkbox-group">
        <label class="checkbox-label">
          <input v-model="form.activo" type="checkbox" />
          <span>Activo</span>
        </label>
      </div>

      <!-- Botones -->
      <div class="form-actions">
        <button
          type="button"
          class="btn btn-secondary"
          @click="cancelar"
          :disabled="guardando"
        >
          Cancelar
        </button>
        <button
          type="submit"
          class="btn btn-primary"
          :disabled="guardando"
        >
          {{ guardando ? 'Guardando...' : 'Guardar' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.servicio-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 1.5rem;
}

.servicio-form h2 {
  margin-bottom: 1.5rem;
  color: var(--color-text);
}

.form-group {
  margin-bottom: 1rem;
  position: relative;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.badge {
  font-size: 0.75rem;
  background-color: var(--color-primary);
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-weight: normal;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.input-error {
  border-color: #ff4444;
}

.field-error {
  color: #ff4444;
  font-size: 0.85rem;
  margin-top: 0.25rem;
  display: block;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.char-count {
  position: absolute;
  right: 0.5rem;
  bottom: -1.25rem;
  font-size: 0.75rem;
  color: #888;
}

textarea.form-input {
  resize: vertical;
  min-height: 120px;
}

/* Selector de categorías */
.categorias-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  min-height: 60px;
  max-height: 200px;
  overflow-y: auto;
}

.loading-small,
.empty-small {
  color: #888;
  font-size: 0.9rem;
  width: 100%;
  text-align: center;
}

.categoria-chip {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  user-select: none;
}

.categoria-chip:hover {
  border-color: var(--color-primary);
}

.categoria-chip.selected {
  background-color: #e8f5e9;
  border-color: var(--color-primary);
  color: #2e7d32;
}

.chip-icono {
  width: 18px;
  height: 18px;
  object-fit: contain;
}

.chip-check {
  font-weight: bold;
  color: var(--color-primary);
}

.checkbox-group {
  margin-top: 1.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input {
  width: 1.25rem;
  height: 1.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #3aa876;
}

.btn-secondary {
  background-color: #e0e0e0;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #d0d0d0;
}
</style>
