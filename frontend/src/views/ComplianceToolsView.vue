<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold mb-4">
              合规工具
            </h1>
            <p class="text-xl text-steel-200 mb-6 lg:mb-0">
              专业的合规管理工具集，助力企业轻松应对各类合规挑战
            </p>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <button class="btn-primary">
              申请定制
            </button>
            <button class="btn-secondary bg-transparent border-2 border-white text-white hover:bg-white hover:text-steel-800">
              联系专家
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 统计概览 -->
    <section class="py-8 bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-6 gap-6">
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-blue mb-2">{{ stats.total_tools || 0 }}</div>
            <div class="text-steel-600">总工具数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-green mb-2">{{ stats.featured_count || 0 }}</div>
            <div class="text-steel-600">推荐工具</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-orange mb-2">{{ stats.verified_count || 0 }}</div>
            <div class="text-steel-600">已验证</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-600 mb-2">{{ stats.popular_count || 0 }}</div>
            <div class="text-steel-600">热门工具</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-600 mb-2">{{ stats.total_usage || 0 }}</div>
            <div class="text-steel-600">总使用量</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-red-600 mb-2">{{ stats.avg_rating || 0 }}</div>
            <div class="text-steel-600">平均评分</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 工具分类导航 -->
    <section class="py-6 bg-steel-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-wrap gap-4 justify-center">
          <button 
            v-for="category in toolCategories" 
            :key="category.key"
            @click="filterByCategory(category.key)"
            :class="[
              'px-6 py-3 rounded-industrial font-medium transition-all duration-200',
              selectedCategory === category.key 
                ? 'bg-accent-blue text-white shadow-lg' 
                : 'bg-white text-steel-700 hover:bg-steel-100 shadow'
            ]"
          >
            <i :class="category.icon" class="mr-2"></i>
            {{ category.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- 筛选和搜索 -->
    <section class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg p-6">
          <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">工具类型</label>
              <select v-model="filters.tool_type" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部类型</option>
                <option value="regulation_checker">法规检查器</option>
                <option value="document_template">文档模板</option>
                <option value="compliance_audit">合规审计</option>
                <option value="risk_assessment">风险评估</option>
                <option value="certification_guide">认证指南</option>
                <option value="export_control">出口管制</option>
                <option value="tariff_calculator">关税计算器</option>
                <option value="legal_database">法律数据库</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">访问级别</label>
              <select v-model="filters.access_level" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部级别</option>
                <option value="free">免费</option>
                <option value="premium">付费</option>
                <option value="enterprise">企业版</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">供应商</label>
              <input 
                v-model="filters.vendor" 
                type="text" 
                placeholder="输入供应商名称..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">最低评分</label>
              <select v-model="filters.min_rating" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">不限</option>
                <option value="4.5">4.5分以上</option>
                <option value="4.0">4.0分以上</option>
                <option value="3.5">3.5分以上</option>
                <option value="3.0">3.0分以上</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">关键词搜索</label>
              <input 
                v-model="filters.keyword" 
                type="text" 
                placeholder="输入关键词..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                @keyup.enter="searchTools"
              />
            </div>
          </div>
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-4">
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_featured" class="mr-2">
                <span class="text-sm text-steel-700">仅显示推荐</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_verified" class="mr-2">
                <span class="text-sm text-steel-700">仅显示已验证</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.trial_available" class="mr-2">
                <span class="text-sm text-steel-700">提供试用</span>
              </label>
            </div>
            <div class="flex gap-4">
              <button @click="resetFilters" class="text-steel-600 hover:text-steel-800">
                重置筛选
              </button>
              <button @click="searchTools" class="btn-primary">
                搜索工具
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 工具列表 -->
    <section class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200 flex justify-between items-center">
            <h3 class="text-lg font-semibold text-steel-800">合规工具列表</h3>
            <div class="flex items-center gap-4">
              <span class="text-sm text-steel-600">排序方式:</span>
              <select v-model="sortBy" @change="searchTools" class="px-3 py-1 border border-steel-300 rounded text-sm">
                <option value="created_at">最新发布</option>
                <option value="rating">评分排序</option>
                <option value="usage_count">使用量</option>
                <option value="price">价格排序</option>
              </select>
            </div>
          </div>
          
          <div v-if="loading" class="p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-blue mx-auto"></div>
            <p class="mt-4 text-steel-600">加载中...</p>
          </div>
          
          <div v-else-if="tools.length === 0" class="p-8 text-center">
            <p class="text-steel-600">暂无合规工具数据</p>
          </div>
          
          <div v-else class="divide-y divide-steel-200">
            <div 
              v-for="tool in tools" 
              :key="tool.id"
              class="p-6 hover:bg-steel-50 transition-colors cursor-pointer"
              @click="viewToolDetail(tool)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-3">
                    <h4 class="text-xl font-semibold text-steel-800 hover:text-accent-blue">
                      {{ tool.name }}
                    </h4>
                    <span v-if="tool.is_featured" class="px-2 py-1 bg-accent-orange text-white text-xs rounded-full">
                      推荐
                    </span>
                    <span v-if="tool.is_verified" class="px-2 py-1 bg-accent-green text-white text-xs rounded-full">
                      已验证
                    </span>
                    <span v-if="tool.is_popular" class="px-2 py-1 bg-purple-600 text-white text-xs rounded-full">
                      热门
                    </span>
                  </div>
                  
                  <p v-if="tool.short_description" class="text-steel-600 mb-3">
                    {{ tool.short_description }}
                  </p>
                  
                  <div class="flex items-center gap-4 mb-3">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getTypeColor(tool.tool_type)
                    ]">
                      {{ getTypeText(tool.tool_type) }}
                    </span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getCategoryColor(tool.category)
                    ]">
                      {{ getCategoryText(tool.category) }}
                    </span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getAccessLevelColor(tool.access_level)
                    ]">
                      {{ getAccessLevelText(tool.access_level) }}
                    </span>
                  </div>
                  
                  <div class="flex items-center gap-6 text-sm text-steel-500 mb-3">
                    <div class="flex items-center">
                      <span class="text-yellow-400 mr-1">★</span>
                      <span>{{ tool.rating }}/5.0 ({{ tool.review_count }}评价)</span>
                    </div>
                    <span>{{ tool.usage_count }} 次使用</span>
                    <span v-if="tool.price > 0">${{ tool.price }}</span>
                    <span v-else class="text-green-600 font-medium">免费</span>
                    <span v-if="tool.trial_available" class="text-blue-600">可试用</span>
                  </div>
                  
                  <div class="text-sm text-steel-600">
                    <span class="font-medium">供应商:</span> {{ tool.vendor || '未知' }}
                    <span class="ml-4 font-medium">版本:</span> {{ tool.version }}
                  </div>
                </div>
                
                <div class="ml-6 text-right">
                  <button class="text-accent-blue hover:text-blue-700 mb-2 block">
                    查看详情 →
                  </button>
                  <button class="text-accent-green hover:text-green-700 text-sm">
                    立即使用
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="tools.length > 0" class="px-6 py-4 border-t border-steel-200 flex justify-between items-center">
            <div class="text-sm text-steel-600">
              显示 {{ tools.length }} 条结果
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
const tools = ref([])
const loading = ref(false)
const sortBy = ref('created_at')
const selectedCategory = ref('')

const filters = ref({
  tool_type: '',
  category: '',
  access_level: '',
  vendor: '',
  keyword: '',
  min_rating: '',
  is_featured: false,
  is_verified: false,
  trial_available: false
})

// 工具分类
const toolCategories = ref([
  { key: '', name: '全部', icon: 'fas fa-th-large' },
  { key: 'trade_compliance', name: '贸易合规', icon: 'fas fa-shipping-fast' },
  { key: 'customs', name: '海关合规', icon: 'fas fa-passport' },
  { key: 'product_safety', name: '产品安全', icon: 'fas fa-shield-alt' },
  { key: 'environmental', name: '环境合规', icon: 'fas fa-leaf' },
  { key: 'data_privacy', name: '数据隐私', icon: 'fas fa-user-shield' },
  { key: 'financial', name: '财务合规', icon: 'fas fa-coins' },
  { key: 'labor_law', name: '劳动法', icon: 'fas fa-users' },
  { key: 'intellectual_property', name: '知识产权', icon: 'fas fa-lightbulb' }
])

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/compliance/stats')
    if (response.ok) {
      stats.value = await response.json()
    } else {
      console.error('获取统计数据失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取合规工具列表
const fetchTools = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.tool_type) params.append('tool_type', filters.value.tool_type)
    if (filters.value.category) params.append('category', filters.value.category)
    if (filters.value.access_level) params.append('access_level', filters.value.access_level)
    if (filters.value.vendor) params.append('vendor', filters.value.vendor)
    if (filters.value.keyword) params.append('keyword', filters.value.keyword)
    if (filters.value.min_rating) params.append('min_rating', filters.value.min_rating)
    if (filters.value.is_featured) params.append('is_featured', 'true')
    if (filters.value.is_verified) params.append('is_verified', 'true')
    if (filters.value.trial_available) params.append('trial_available', 'true')
    params.append('sort_by', sortBy.value)
    params.append('sort_order', 'desc')
    
    const response = await fetch(`http://localhost:8000/api/v1/compliance/?${params.toString()}`)
    if (response.ok) {
      tools.value = await response.json()
    } else {
      console.error('获取合规工具失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取合规工具失败:', error)
  } finally {
    loading.value = false
  }
}

// 按分类筛选
const filterByCategory = (category: string) => {
  selectedCategory.value = category
  filters.value.category = category
  fetchTools()
}

// 搜索工具
const searchTools = () => {
  fetchTools()
}

// 重置筛选
const resetFilters = () => {
  filters.value = {
    tool_type: '',
    category: '',
    access_level: '',
    vendor: '',
    keyword: '',
    min_rating: '',
    is_featured: false,
    is_verified: false,
    trial_available: false
  }
  selectedCategory.value = ''
  fetchTools()
}

// 加载更多
const loadMore = () => {
  // TODO: 实现分页加载
  console.log('加载更多')
}

// 查看工具详情
const viewToolDetail = (tool: any) => {
  // TODO: 跳转到工具详情页面
  console.log('查看工具详情:', tool)
}

// 工具函数
const getTypeColor = (type: string) => {
  const colors = {
    'regulation_checker': 'bg-blue-100 text-blue-800',
    'document_template': 'bg-green-100 text-green-800',
    'compliance_audit': 'bg-yellow-100 text-yellow-800',
    'risk_assessment': 'bg-red-100 text-red-800',
    'certification_guide': 'bg-purple-100 text-purple-800',
    'export_control': 'bg-orange-100 text-orange-800',
    'tariff_calculator': 'bg-indigo-100 text-indigo-800',
    'legal_database': 'bg-pink-100 text-pink-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getTypeText = (type: string) => {
  const texts = {
    'regulation_checker': '法规检查器',
    'document_template': '文档模板',
    'compliance_audit': '合规审计',
    'risk_assessment': '风险评估',
    'certification_guide': '认证指南',
    'export_control': '出口管制',
    'tariff_calculator': '关税计算器',
    'legal_database': '法律数据库'
  }
  return texts[type] || type
}

const getCategoryColor = (category: string) => {
  const colors = {
    'trade_compliance': 'bg-blue-100 text-blue-800',
    'product_safety': 'bg-green-100 text-green-800',
    'environmental': 'bg-emerald-100 text-emerald-800',
    'data_privacy': 'bg-purple-100 text-purple-800',
    'financial': 'bg-yellow-100 text-yellow-800',
    'labor_law': 'bg-orange-100 text-orange-800',
    'intellectual_property': 'bg-pink-100 text-pink-800',
    'customs': 'bg-indigo-100 text-indigo-800'
  }
  return colors[category] || 'bg-gray-100 text-gray-800'
}

const getCategoryText = (category: string) => {
  const texts = {
    'trade_compliance': '贸易合规',
    'product_safety': '产品安全',
    'environmental': '环境合规',
    'data_privacy': '数据隐私',
    'financial': '财务合规',
    'labor_law': '劳动法',
    'intellectual_property': '知识产权',
    'customs': '海关合规'
  }
  return texts[category] || category
}

const getAccessLevelColor = (level: string) => {
  const colors = {
    'free': 'bg-green-100 text-green-800',
    'premium': 'bg-blue-100 text-blue-800',
    'enterprise': 'bg-purple-100 text-purple-800'
  }
  return colors[level] || 'bg-gray-100 text-gray-800'
}

const getAccessLevelText = (level: string) => {
  const texts = {
    'free': '免费',
    'premium': '付费',
    'enterprise': '企业版'
  }
  return texts[level] || level
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  fetchTools()
})
</script>
