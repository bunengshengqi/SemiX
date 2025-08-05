import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  is_verified: boolean
}

export interface LoginCredentials {
  username: string
  password: string
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_superuser || false)

  // 登录
  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    error.value = null

    try {
      const formData = new FormData()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)

      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '登录失败')
      }

      const data = await response.json()
      token.value = data.access_token
      localStorage.setItem('access_token', data.access_token)

      // 获取用户信息
      await fetchUserInfo()

      return true
    } catch (err: any) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    if (!token.value) return

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${token.value}`,
        },
      })

      if (response.ok) {
        user.value = await response.json()
      } else {
        // Token可能已过期
        logout()
      }
    } catch (err) {
      console.error('获取用户信息失败:', err)
      logout()
    }
  }

  // 登出
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    error.value = null
  }

  // 初始化时检查登录状态
  const initialize = async () => {
    if (token.value) {
      await fetchUserInfo()
    }
  }

  return {
    // 状态
    user,
    token,
    loading,
    error,
    
    // 计算属性
    isAuthenticated,
    isAdmin,
    
    // 方法
    login,
    logout,
    fetchUserInfo,
    initialize,
  }
})
