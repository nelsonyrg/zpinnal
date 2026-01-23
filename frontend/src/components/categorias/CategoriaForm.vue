<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useCategoriaStore } from '@/stores/categoriaStore'
import type { Categoria, CategoriaCreate, CategoriaUpdate } from '@/types/categoria'

const props = defineProps<{
  categoria?: Categoria | null
  modo: 'crear' | 'editar'
}>()

const emit = defineEmits<{
  (e: 'guardado', categoria: Categoria): void
  (e: 'cancelado'): void
}>()

const store = useCategoriaStore()

// Estado del formulario
const form = ref<CategoriaCreate>({
  nombre: '',
  descripcion: '',
  icono: '',
  activo: true,
  categoria_padre_id: null
})

const errores = ref<Record<string, string>>({})
const guardando = ref(false)

// Título del formulario
const titulo = computed(() =>
  props.modo === 'crear' ? 'Nueva Categoría' : 'Editar Categoría'
)

// Categorías disponibles para selector de padre (excluyendo la actual si es edición)
const categoriasPadreDisponibles = computed(() => {
  return store.categorias.filter(c => {
    if (props.modo === 'editar' && props.categoria) {
      return c.id !== props.categoria.id
    }
    return true
  })
})

// Cargar datos si es edición
watch(() => props.categoria, (nuevaCategoria) => {
  if (nuevaCategoria && props.modo === 'editar') {
    form.value = {
      nombre: nuevaCategoria.nombre,
      descripcion: nuevaCategoria.descripcion || '',
      icono: nuevaCategoria.icono || '',
      activo: nuevaCategoria.activo,
      categoria_padre_id: nuevaCategoria.categoria_padre_id
    }
  }
}, { immediate: true })

// Validación
function validar(): boolean {
  errores.value = {}

  if (!form.value.nombre.trim()) {
    errores.value.nombre = 'El nombre es requerido'
  } else if (form.value.nombre.length > 150) {
    errores.value.nombre = 'El nombre no puede exceder 150 caracteres'
  }

  if (form.value.descripcion && form.value.descripcion.length > 1000) {
    errores.value.descripcion = 'La descripción no puede exceder 1000 caracteres'
  }

  if (form.value.icono && form.value.icono.length > 700) {
    errores.value.icono = 'La ruta del icono no puede exceder 700 caracteres'
  }

  return Object.keys(errores.value).length === 0
}

// Guardar
async function guardar() {
  if (!validar()) return

  guardando.value = true
  try {
    let resultado: Categoria

    if (props.modo === 'crear') {
      resultado = await store.crearCategoria(form.value)
    } else {
      const updateData: CategoriaUpdate = { ...form.value }
      resultado = await store.actualizarCategoria(props.categoria!.id, updateData)
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

// Cancelar
function cancelar() {
  emit('cancelado')
}

// Cargar categorías para el selector
onMounted(async () => {
  if (store.categorias.length === 0) {
    await store.cargarCategorias()
  }
})
</script>

<template>
  <div class="categoria-form">
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
          maxlength="150"
          placeholder="Nombre de la categoría"
        />
        <span v-if="errores.nombre" class="field-error">{{ errores.nombre }}</span>
        <span class="char-count">{{ form.nombre.length }}/150</span>
      </div>

      <!-- Descripción -->
      <div class="form-group">
        <label for="descripcion" class="form-label">Descripción</label>
        <textarea
          id="descripcion"
          v-model="form.descripcion"
          class="form-input"
          :class="{ 'input-error': errores.descripcion }"
          maxlength="1000"
          rows="4"
          placeholder="Descripción de la categoría"
        ></textarea>
        <span v-if="errores.descripcion" class="field-error">{{ errores.descripcion }}</span>
        <span class="char-count">{{ form.descripcion?.length || 0 }}/1000</span>
      </div>

      <!-- Icono -->
      <div class="form-group">
        <label for="icono" class="form-label">Ruta del Icono</label>
        <input
          id="icono"
          v-model="form.icono"
          type="text"
          class="form-input"
          :class="{ 'input-error': errores.icono }"
          maxlength="700"
          placeholder="/icons/categoria.svg"
        />
        <span v-if="errores.icono" class="field-error">{{ errores.icono }}</span>
      </div>

      <!-- Categoría Padre -->
      <div class="form-group">
        <label for="categoria_padre" class="form-label">Categoría Padre</label>
        <select
          id="categoria_padre"
          v-model="form.categoria_padre_id"
          class="form-input"
        >
          <option :value="null">-- Sin categoría padre --</option>
          <option
            v-for="cat in categoriasPadreDisponibles"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.nombre }}
          </option>
        </select>
      </div>

      <!-- Activo -->
      <div class="form-group checkbox-group">
        <label class="checkbox-label">
          <input
            v-model="form.activo"
            type="checkbox"
          />
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
.categoria-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 1.5rem;
}

.categoria-form h2 {
  margin-bottom: 1.5rem;
  color: var(--color-text);
}

.form-group {
  margin-bottom: 1rem;
  position: relative;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
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

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}
</style>
