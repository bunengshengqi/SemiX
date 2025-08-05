<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold mb-4">
              政策监控台
            </h1>
            <p class="text-xl text-steel-200 mb-6 lg:mb-0">
              实时监控日韩新台政策变化，助力企业合规出海
            </p>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <button class="btn-primary">
              订阅政策提醒
            </button>
            <button class="btn-secondary bg-transparent border-2 border-white text-white hover:bg-white hover:text-steel-800">
              导出报告
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 统计概览 -->
    <section class="py-8 bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-blue mb-2">{{ stats.total_policies || 0 }}</div>
            <div class="text-steel-600">总政策数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-orange mb-2">{{ stats.recent_updates || 0 }}</div>
            <div class="text-steel-600">本周更新</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-green mb-2">{{ Object.keys(stats.by_country || {}).length }}</div>
            <div class="text-steel-600">覆盖地区</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-red-600 mb-2">{{ stats.by_urgency?.high || 0 }}</div>
            <div class="text-steel-600">高优先级</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 筛选和搜索 -->
    <section class="py-6 bg-steel-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg p-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">国家/地区</label>
              <select v-model="filters.country" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部地区</option>
                <option value="日本">日本</option>
                <option value="韩国">韩国</option>
                <option value="台湾省">台湾省</option>
                <option value="东南亚">东南亚</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">政策类别</label>
              <select v-model="filters.category" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部类别</option>
                <option value="export_control">出口管制</option>
                <option value="trade_policy">贸易政策</option>
                <option value="investment">投资政策</option>
                <option value="taxation">税收政策</option>
                <option value="regulation">法规政策</option>
                <option value="compliance">合规要求</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">紧急程度</label>
              <select v-model="filters.urgency" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部级别</option>
                <option value="critical">紧急</option>
                <option value="high">高</option>
                <option value="medium">中</option>
                <option value="low">低</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">关键词搜索</label>
              <input 
                v-model="filters.keyword" 
                type="text" 
                placeholder="输入关键词..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                @keyup.enter="searchPolicies"
              />
            </div>
          </div>
          <div class="flex justify-between items-center">
            <button @click="resetFilters" class="text-steel-600 hover:text-steel-800">
              重置筛选
            </button>
            <button @click="searchPolicies" class="btn-primary">
              搜索政策
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 政策列表 -->
    <section class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200">
            <h3 class="text-lg font-semibold text-steel-800">政策列表</h3>
          </div>
          
          <div v-if="loading" class="p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-blue mx-auto"></div>
            <p class="mt-4 text-steel-600">加载中...</p>
          </div>
          
          <div v-else-if="policies.length === 0" class="p-8 text-center">
            <p class="text-steel-600">暂无政策数据</p>
          </div>
          
          <div v-else class="divide-y divide-steel-200">
            <div 
              v-for="policy in policies" 
              :key="policy.id"
              class="p-6 hover:bg-steel-50 transition-colors cursor-pointer"
              @click="viewPolicyDetail(policy)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-2">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getCountryColor(policy.country)
                    ]">
                      {{ policy.country }}
                    </span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getUrgencyColor(policy.urgency)
                    ]">
                      {{ getUrgencyText(policy.urgency) }}
                    </span>
                    <span class="text-xs text-steel-500">
                      {{ formatDate(policy.created_at) }}
                    </span>
                  </div>
                  <h4 class="text-lg font-semibold text-steel-800 mb-2 hover:text-accent-blue">
                    {{ policy.title }}
                  </h4>
                  <p class="text-steel-600 mb-3">
                    {{ policy.summary }}
                  </p>
                  <div class="flex items-center gap-4 text-sm text-steel-500">
                    <span>影响评分: {{ policy.impact_score }}/100</span>
                    <span>政策编号: {{ policy.policy_number || 'N/A' }}</span>
                    <span v-if="policy.effective_date">
                      生效日期: {{ formatDate(policy.effective_date) }}
                    </span>
                  </div>
                </div>
                <div class="ml-4">
                  <button class="text-accent-blue hover:text-blue-700">
                    查看详情 →
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="policies.length > 0" class="px-6 py-4 border-t border-steel-200 flex justify-between items-center">
            <div class="text-sm text-steel-600">
              显示 {{ policies.length }} 条结果
            </div>
            <div class="flex gap-2">
              <button 
                @click="loadMore" 
                :disabled="loading"
                class="btn-secondary text-sm"
              >
                加载更多
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 响应式数据
const stats = ref({})
const policies = ref([])
const loading = ref(false)
const filters = ref({
  country: '',
  category: '',
  urgency: '',
  keyword: ''
})

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/policies/stats')
    if (response.ok) {
      stats.value = await response.json()
    } else {
      console.error('获取统计数据失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取政策列表
const fetchPolicies = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.country) params.append('country', filters.value.country)
    if (filters.value.category) params.append('category', filters.value.category)
    if (filters.value.urgency) params.append('urgency', filters.value.urgency)
    if (filters.value.keyword) params.append('keyword', filters.value.keyword)

    const response = await fetch(`http://localhost:8000/api/v1/policies/?${params.toString()}`)
    if (response.ok) {
      policies.value = await response.json()
    } else {
      console.error('获取政策列表失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取政策列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索政策
const searchPolicies = () => {
  fetchPolicies()
}

// 重置筛选
const resetFilters = () => {
  filters.value = {
    country: '',
    category: '',
    urgency: '',
    keyword: ''
  }
  fetchPolicies()
}

// 加载更多
const loadMore = () => {
  // TODO: 实现分页加载
  console.log('加载更多')
}

// 查看政策详情
const viewPolicyDetail = (policy: any) => {
  // TODO: 跳转到政策详情页面
  console.log('查看政策详情:', policy)
}

// 工具函数
const getCountryColor = (country: string) => {
  const colors = {
    '日本': 'bg-blue-100 text-blue-800',
    '韩国': 'bg-green-100 text-green-800',
    '台湾省': 'bg-orange-100 text-orange-800',
    '东南亚': 'bg-purple-100 text-purple-800'
  }
  return colors[country] || 'bg-gray-100 text-gray-800'
}

const getUrgencyColor = (urgency: string) => {
  const colors = {
    'critical': 'bg-red-100 text-red-800',
    'high': 'bg-orange-100 text-orange-800',
    'medium': 'bg-yellow-100 text-yellow-800',
    'low': 'bg-green-100 text-green-800'
  }
  return colors[urgency] || 'bg-gray-100 text-gray-800'
}

const getUrgencyText = (urgency: string) => {
  const texts = {
    'critical': '紧急',
    'high': '高',
    'medium': '中',
    'low': '低'
  }
  return texts[urgency] || urgency
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  fetchPolicies()
})
</script>
