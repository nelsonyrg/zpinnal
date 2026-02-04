<script setup lang="ts">
import { ref } from 'vue'
import ServicioLista from '@/components/servicios/ServicioLista.vue'
import ServicioForm from '@/components/servicios/ServicioForm.vue'
import type { Servicio } from '@/types/servicio'

type ModoVista = 'lista' | 'crear' | 'editar'
const modoVista = ref<ModoVista>('lista')
const servicioSeleccionado = ref<Servicio | null>(null)

function nuevoServicio() {
  servicioSeleccionado.value = null
  modoVista.value = 'crear'
}

function editarServicio(servicio: Servicio) {
  servicioSeleccionado.value = servicio
  modoVista.value = 'editar'
}

function volverALista() {
  modoVista.value = 'lista'
  servicioSeleccionado.value = null
}

function onGuardado() {
  volverALista()
}
</script>

<template>
  <div class="servicios-view">
    <ServicioLista
      v-if="modoVista === 'lista'"
      @nuevo="nuevoServicio"
      @editar="editarServicio"
    />

    <div v-else class="form-container">
      <button class="btn-volver" @click="volverALista">
        ← Volver a la lista
      </button>

      <ServicioForm
        :servicio="servicioSeleccionado"
        :modo="modoVista === 'crear' ? 'crear' : 'editar'"
        @guardado="onGuardado"
        @cancelado="volverALista"
      />
    </div>
  </div>
</template>

<style scoped>
.servicios-view {
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
