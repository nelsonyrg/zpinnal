<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService } from '@/services/api'

const healthStatus = ref<string>('Verificando...')
const apiVersion = ref<string>('')

onMounted(async () => {
  try {
    const response = await apiService.healthCheck()
    healthStatus.value = response.status
    apiVersion.value = response.version || ''
  } catch {
    healthStatus.value = 'Error de conexión'
  }
})
</script>

<template>
  <div class="home">
    <h1>Mobile App</h1>
    <p>Aplicación Vue.js + Capacitor con backend FastAPI</p>

    <div class="status-card">
      <h2>Estado del Backend</h2>
      <p>
        Status: <strong :class="healthStatus === 'healthy' ? 'success' : 'error'">
          {{ healthStatus }}
        </strong>
      </p>
      <p v-if="apiVersion">Versión: {{ apiVersion }}</p>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
}

.status-card {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
  background-color: #f5f5f5;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.success {
  color: #42b883;
}

.error {
  color: #ff4444;
}
</style>
