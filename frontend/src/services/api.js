import axios from 'axios'

// Determine API base URL based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV ? 'http://localhost:5000' : '/api')

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Authentication
export const login = async (name, phone) => {
  try {
    const response = await api.post('/login', { name, phone })
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Login failed' }
  }
}

// Employee operations
export const getEmployeeDetails = async (employeeId) => {
  try {
    const response = await api.get(`/employee/details/${employeeId}`)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to get employee details' }
  }
}

export const getBooks = async () => {
  try {
    const response = await api.get('/books')
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to get books' }
  }
}

export const takeBook = async (employeeId, bookId) => {
  try {
    const response = await api.post('/take-book', { employee_id: employeeId, book_id: bookId })
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to take book' }
  }
}

// Admin operations
export const getAdminData = async () => {
  try {
    const response = await api.get('/admin/data')
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to get admin data' }
  }
}

export const getAllEmployees = async () => {
  try {
    const response = await api.get('/admin/employees')
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to get employees' }
  }
}

export const createEmployee = async (employeeData) => {
  try {
    const response = await api.post('/admin/employees', employeeData)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to create employee' }
  }
}

export const updateEmployee = async (employeeId, employeeData) => {
  try {
    const response = await api.put(`/admin/employees/${employeeId}`, employeeData)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to update employee' }
  }
}

export const deleteEmployee = async (employeeId) => {
  try {
    const response = await api.delete(`/admin/employees/${employeeId}`)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to delete employee' }
  }
}

export const getAllBooks = async () => {
  try {
    const response = await api.get('/admin/books')
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to get books' }
  }
}

export const createBook = async (bookData) => {
  try {
    const response = await api.post('/admin/books', bookData)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to create book' }
  }
}

export const updateBook = async (bookId, bookData) => {
  try {
    const response = await api.put(`/admin/books/${bookId}`, bookData)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to update book' }
  }
}

export const deleteBook = async (bookId) => {
  try {
    const response = await api.delete(`/admin/books/${bookId}`)
    return response.data
  } catch (error) {
    throw error.response?.data || { message: 'Failed to delete book' }
  }
}

export default api
