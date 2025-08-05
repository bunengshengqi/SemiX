<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold mb-4">
              供应商目录
            </h1>
            <p class="text-xl text-steel-200 mb-6 lg:mb-0">
              精选全球优质半导体供应商，助力企业找到最佳合作伙伴
            </p>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <button class="btn-primary">
              申请入驻
            </button>
            <button class="btn-secondary bg-transparent border-2 border-white text-white hover:bg-white hover:text-steel-800">
              下载目录
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 统计概览 -->
    <section class="py-8 bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-blue mb-2">{{ stats.total_suppliers || 0 }}</div>
            <div class="text-steel-600">总供应商数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-green mb-2">{{ stats.verified_count || 0 }}</div>
            <div class="text-steel-600">已认证</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-orange mb-2">{{ stats.featured_count || 0 }}</div>
            <div class="text-steel-600">推荐供应商</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-600 mb-2">{{ Object.keys(stats.by_country || {}).length }}</div>
            <div class="text-steel-600">覆盖地区</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-600 mb-2">{{ stats.avg_rating || 0 }}</div>
            <div class="text-steel-600">平均评分</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 筛选和搜索 -->
    <section class="py-6 bg-steel-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg p-6">
          <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
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
              <label class="block text-sm font-medium text-steel-700 mb-2">供应商类型</label>
              <select v-model="filters.supplier_type" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部类型</option>
                <option value="manufacturer">制造商</option>
                <option value="distributor">分销商</option>
                <option value="trader">贸易商</option>
                <option value="service_provider">服务商</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">企业规模</label>
              <select v-model="filters.scale" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部规模</option>
                <option value="large">大型企业</option>
                <option value="medium">中型企业</option>
                <option value="small">小型企业</option>
                <option value="startup">初创企业</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">认证级别</label>
              <select v-model="filters.certification_level" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部级别</option>
                <option value="premium">金牌认证</option>
                <option value="verified">认证供应商</option>
                <option value="basic">基础认证</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">关键词搜索</label>
              <input 
                v-model="filters.keyword" 
                type="text" 
                placeholder="输入关键词..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                @keyup.enter="searchSuppliers"
              />
            </div>
          </div>
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-4">
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_verified" class="mr-2">
                <span class="text-sm text-steel-700">仅显示已认证</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_featured" class="mr-2">
                <span class="text-sm text-steel-700">仅显示推荐</span>
              </label>
            </div>
            <div class="flex gap-4">
              <button @click="resetFilters" class="text-steel-600 hover:text-steel-800">
                重置筛选
              </button>
              <button @click="searchSuppliers" class="btn-primary">
                搜索供应商
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 供应商列表 -->
    <section class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200 flex justify-between items-center">
            <h3 class="text-lg font-semibold text-steel-800">供应商列表</h3>
            <div class="flex items-center gap-4">
              <span class="text-sm text-steel-600">排序方式:</span>
              <select v-model="sortBy" @change="searchSuppliers" class="px-3 py-1 border border-steel-300 rounded text-sm">
                <option value="overall_rating">综合评分</option>
                <option value="review_count">评价数量</option>
                <option value="created_at">最新入驻</option>
                <option value="annual_revenue">企业规模</option>
              </select>
            </div>
          </div>
          
          <div v-if="loading" class="p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-blue mx-auto"></div>
            <p class="mt-4 text-steel-600">加载中...</p>
          </div>
          
          <div v-else-if="suppliers.length === 0" class="p-8 text-center">
            <p class="text-steel-600">暂无供应商数据</p>
          </div>
          
          <div v-else class="divide-y divide-steel-200">
            <div 
              v-for="supplier in suppliers" 
              :key="supplier.id"
              class="p-6 hover:bg-steel-50 transition-colors cursor-pointer"
              @click="viewSupplierDetail(supplier)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-3">
                    <h4 class="text-xl font-semibold text-steel-800 hover:text-accent-blue">
                      {{ supplier.company_name }}
                    </h4>
                    <span v-if="supplier.is_featured" class="px-2 py-1 bg-accent-orange text-white text-xs rounded-full">
                      推荐
                    </span>
                    <span v-if="supplier.is_verified" class="px-2 py-1 bg-accent-green text-white text-xs rounded-full">
                      已认证
                    </span>
                  </div>
                  
                  <div class="flex items-center gap-4 mb-3">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getCountryColor(supplier.country)
                    ]">
                      {{ supplier.country }}
                    </span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getTypeColor(supplier.supplier_type)
                    ]">
                      {{ getTypeText(supplier.supplier_type) }}
                    </span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getCertificationColor(supplier.certification_level)
                    ]">
                      {{ getCertificationText(supplier.certification_level) }}
                    </span>
                  </div>
                  
                  <p class="text-steel-600 mb-3">
                    {{ supplier.company_description || '暂无描述' }}
                  </p>
                  
                  <div class="flex items-center gap-6 text-sm text-steel-500 mb-3">
                    <div class="flex items-center">
                      <span class="text-yellow-400 mr-1">★</span>
                      <span>{{ supplier.overall_rating }}/5.0 ({{ supplier.review_count }}评价)</span>
                    </div>
                    <span>成立于{{ supplier.established_year }}年</span>
                    <span v-if="supplier.employee_count">员工{{ supplier.employee_count }}人</span>
                  </div>
                  
                  <div class="text-sm text-steel-600">
                    <span class="font-medium">主营产品:</span>
                    {{ getMainProducts(supplier.main_products) }}
                  </div>
                </div>
                
                <div class="ml-6 text-right">
                  <button class="text-accent-blue hover:text-blue-700 mb-2 block">
                    查看详情 →
                  </button>
                  <button class="text-accent-green hover:text-green-700 text-sm">
                    联系供应商
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="suppliers.length > 0" class="px-6 py-4 border-t border-steel-200 flex justify-between items-center">
            <div class="text-sm text-steel-600">
              显示 {{ suppliers.length }} 条结果
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
const suppliers = ref([])
const loading = ref(false)
const sortBy = ref('overall_rating')
const filters = ref({
  country: '',
  supplier_type: '',
  scale: '',
  certification_level: '',
  keyword: '',
  is_verified: false,
  is_featured: false
})

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/suppliers/stats')
    if (response.ok) {
      stats.value = await response.json()
    } else {
      console.error('获取统计数据失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取供应商列表
const fetchSuppliers = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.country) params.append('country', filters.value.country)
    if (filters.value.supplier_type) params.append('supplier_type', filters.value.supplier_type)
    if (filters.value.scale) params.append('scale', filters.value.scale)
    if (filters.value.certification_level) params.append('certification_level', filters.value.certification_level)
    if (filters.value.keyword) params.append('keyword', filters.value.keyword)
    if (filters.value.is_verified) params.append('is_verified', 'true')
    if (filters.value.is_featured) params.append('is_featured', 'true')
    params.append('sort_by', sortBy.value)
    params.append('sort_order', 'desc')
    
    const response = await fetch(`http://localhost:8000/api/v1/suppliers/?${params.toString()}`)
    if (response.ok) {
      suppliers.value = await response.json()
    } else {
      console.error('获取供应商列表失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取供应商列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索供应商
const searchSuppliers = () => {
  fetchSuppliers()
}

// 重置筛选
const resetFilters = () => {
  filters.value = {
    country: '',
    supplier_type: '',
    scale: '',
    certification_level: '',
    keyword: '',
    is_verified: false,
    is_featured: false
  }
  fetchSuppliers()
}

// 加载更多
const loadMore = () => {
  // TODO: 实现分页加载
  console.log('加载更多')
}

// 查看供应商详情
const viewSupplierDetail = (supplier: any) => {
  // TODO: 跳转到供应商详情页面
  console.log('查看供应商详情:', supplier)
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

const getTypeColor = (type: string) => {
  const colors = {
    'manufacturer': 'bg-blue-100 text-blue-800',
    'distributor': 'bg-green-100 text-green-800',
    'trader': 'bg-yellow-100 text-yellow-800',
    'service_provider': 'bg-purple-100 text-purple-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getTypeText = (type: string) => {
  const texts = {
    'manufacturer': '制造商',
    'distributor': '分销商',
    'trader': '贸易商',
    'service_provider': '服务商'
  }
  return texts[type] || type
}

const getCertificationColor = (level: string) => {
  const colors = {
    'premium': 'bg-yellow-100 text-yellow-800',
    'verified': 'bg-green-100 text-green-800',
    'basic': 'bg-blue-100 text-blue-800',
    'unverified': 'bg-gray-100 text-gray-800'
  }
  return colors[level] || 'bg-gray-100 text-gray-800'
}

const getCertificationText = (level: string) => {
  const texts = {
    'premium': '金牌认证',
    'verified': '认证供应商',
    'basic': '基础认证',
    'unverified': '未认证'
  }
  return texts[level] || level
}

const getMainProducts = (productsJson: string) => {
  try {
    const products = JSON.parse(productsJson)
    return Array.isArray(products) ? products.slice(0, 3).join('、') : productsJson
  } catch {
    return productsJson
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  fetchSuppliers()
})
</script>
