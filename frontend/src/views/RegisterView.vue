<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <div class="mx-auto h-12 w-12 bg-accent-orange rounded-full flex items-center justify-center">
          <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
        </div>
        <h2 class="mt-6 text-center text-3xl font-bold text-steel-800">
          创建新账户
        </h2>
        <div v-if="form.trialPlan" class="mt-4 text-center">
          <div class="inline-flex items-center bg-accent-orange bg-opacity-10 text-accent-orange px-4 py-2 rounded-full text-sm font-medium">
            <span class="mr-2">🎉</span>
            已选择{{ form.trialPlan === 'basic' ? '基础' : form.trialPlan === 'professional' ? '专业' : '企业' }}试用套餐
          </div>
        </div>
        <p class="mt-2 text-center text-sm text-steel-600">
          已有账户？
          <RouterLink to="/login" class="font-medium text-accent-blue hover:text-blue-600">
            立即登录
          </RouterLink>
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="username" class="block text-sm font-medium text-steel-700">
                用户名
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                v-model="form.username"
                class="mt-1 appearance-none relative block w-full px-3 py-2 border border-steel-300 placeholder-steel-500 text-steel-900 rounded-industrial focus:outline-none focus:ring-accent-blue focus:border-accent-blue focus:z-10 sm:text-sm"
                placeholder="用户名"
              />
            </div>
            
            <div>
              <label for="full_name" class="block text-sm font-medium text-steel-700">
                姓名
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                v-model="form.full_name"
                class="mt-1 appearance-none relative block w-full px-3 py-2 border border-steel-300 placeholder-steel-500 text-steel-900 rounded-industrial focus:outline-none focus:ring-accent-blue focus:border-accent-blue focus:z-10 sm:text-sm"
                placeholder="真实姓名"
              />
            </div>
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-steel-700">
              邮箱地址
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              required
              v-model="form.email"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-steel-300 placeholder-steel-500 text-steel-900 rounded-industrial focus:outline-none focus:ring-accent-blue focus:border-accent-blue focus:z-10 sm:text-sm"
              placeholder="请输入邮箱地址"
            />
          </div>
          
          <div>
            <label for="company" class="block text-sm font-medium text-steel-700">
              公司名称（可选）
            </label>
            <input
              id="company"
              name="company"
              type="text"
              v-model="form.company"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-steel-300 placeholder-steel-500 text-steel-900 rounded-industrial focus:outline-none focus:ring-accent-blue focus:border-accent-blue focus:z-10 sm:text-sm"
              placeholder="公司名称"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-steel-700">
              密码
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="new-password"
              required
              v-model="form.password"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-steel-300 placeholder-steel-500 text-steel-900 rounded-industrial focus:outline-none focus:ring-accent-blue focus:border-accent-blue focus:z-10 sm:text-sm"
              placeholder="请输入密码（至少8位）"
            />
          </div>
          
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-steel-700">
              确认密码
            </label>
            <input
              id="confirm_password"
              name="confirm_password"
              type="password"
              autocomplete="new-password"
              required
              v-model="form.confirm_password"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-steel-300 placeholder-steel-500 text-steel-900 rounded-industrial focus:outline-none focus:ring-accent-blue focus:border-accent-blue focus:z-10 sm:text-sm"
              placeholder="请再次输入密码"
            />
          </div>
        </div>

        <div class="flex items-center">
          <input
            id="agree-terms"
            name="agree-terms"
            type="checkbox"
            required
            v-model="form.agreeTerms"
            class="h-4 w-4 text-accent-blue focus:ring-accent-blue border-steel-300 rounded"
          />
          <label for="agree-terms" class="ml-2 block text-sm text-steel-700">
            我同意
            <a href="#" class="text-accent-blue hover:text-blue-600">服务条款</a>
            和
            <a href="#" class="text-accent-blue hover:text-blue-600">隐私政策</a>
          </label>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-industrial text-white bg-accent-orange hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-orange disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ loading ? '注册中...' : '免费注册' }}
          </button>
        </div>

        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { RouterLink } from 'vue-router'

const router = useRouter()
const route = useRoute()

const form = ref({
  username: '',
  full_name: '',
  email: '',
  company: '',
  password: '',
  confirm_password: '',
  agreeTerms: false,
  trialPlan: ''
})

const loading = ref(false)
const error = ref('')

// 检查URL参数中的试用套餐
onMounted(() => {
  const plan = route.query.plan as string
  if (plan && ['basic', 'professional', 'enterprise'].includes(plan)) {
    form.value.trialPlan = plan
  }
})

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // 验证密码匹配
    if (form.value.password !== form.value.confirm_password) {
      throw new Error('密码和确认密码不匹配')
    }
    
    // 验证密码长度
    if (form.value.password.length < 8) {
      throw new Error('密码长度至少为8位')
    }
    
    // TODO: 实现注册逻辑
    console.log('注册表单数据:', form.value)
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 注册成功后跳转到登录页
    router.push('/login')
  } catch (err: any) {
    error.value = err.message || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
