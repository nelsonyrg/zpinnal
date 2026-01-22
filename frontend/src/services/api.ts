import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const apiService = {
  async healthCheck() {
    const response = await apiClient.get('/health')
    return response.data
  },

  async getUsers() {
    const response = await apiClient.get('/users')
    return response.data
  },

  async getUser(id: number) {
    const response = await apiClient.get(`/users/${id}`)
    return response.data
  },

  async createUser(userData: { email: string; username: string; password: string }) {
    const response = await apiClient.post('/users', userData)
    return response.data
  }
}

export default apiClient
