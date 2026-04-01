import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const api = {
  // Projects - Public
  getProjects: () => client.get('/projects'),
  getProject: (id) => client.get(`/projects/${id}`),

  // Projects - Admin
  createProject: (data) => client.post('/projects', data),
  updateProject: (id, data) => client.put(`/projects/${id}`, data),
  deleteProject: (id) => client.delete(`/projects/${id}`),

  // Auth
  login: (credentials) => client.post('/auth/login', credentials),
  getCurrentUser: () => client.get('/auth/me'),

  // Health
  health: () => client.get('/health'),
}

export default client
