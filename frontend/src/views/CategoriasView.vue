<script setup lang="ts">
import { ref } from 'vue'
import CategoriaLista from '@/components/categorias/CategoriaLista.vue'
import CategoriaForm from '@/components/categorias/CategoriaForm.vue'
import type { Categoria } from '@/types/categoria'

// Estado de la vista
type ModoVista = 'lista' | 'crear' | 'editar'
const modoVista = ref<ModoVista>('lista')
const categoriaSeleccionada = ref<Categoria | null>(null)

// Cambiar a modo crear
function nuevaCategoria() {
  categoriaSeleccionada.value = null
  modoVista.value = 'crear'
}

// Cambiar a modo editar
function editarCategoria(categoria: Categoria) {
  categoriaSeleccionada.value = categoria
  modoVista.value = 'editar'
}

// Volver a la lista
function volverALista() {
  modoVista.value = 'lista'
  categoriaSeleccionada.value = null
}

// Cuando se guarda exitosamente
function onGuardado(categoria: Categoria) {
  console.log('Categoría guardada:', categoria)
  volverALista()
}
</script>

<template>
  <div class="categorias-view">
    <!-- Vista de lista -->
    <CategoriaLista
      v-if="modoVista === 'lista'"
      @nueva="nuevaCategoria"
      @editar="editarCategoria"
    />

    <!-- Vista de formulario (crear/editar) -->
    <div v-else class="form-container">
      <button class="btn-volver" @click="volverALista">
        ← Volver a la lista
      </button>

      <CategoriaForm
        :categoria="categoriaSeleccionada"
        :modo="modoVista === 'crear' ? 'crear' : 'editar'"
        @guardado="onGuardado"
        @cancelado="volverALista"
      />
    </div>
  </div>
</template>

<style scoped>
.categorias-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.form-container {
  max-width: 700px;
  margin: 0 auto;
}

.btn-volver {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.5rem 0;
  margin-bottom: 1rem;
}

.btn-volver:hover {
  text-decoration: underline;
}
</style>
