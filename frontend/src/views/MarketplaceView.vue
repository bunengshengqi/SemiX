<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold mb-4">
              二手交易市场
            </h1>
            <p class="text-xl text-steel-200 mb-6 lg:mb-0">
              全球半导体器件交易平台，买卖双方安全可靠的交易环境
            </p>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <button class="btn-primary">
              发布交易
            </button>
            <button class="btn-secondary bg-transparent border-2 border-white text-white hover:bg-white hover:text-steel-800">
              我的交易
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
            <div class="text-3xl font-bold text-accent-blue mb-2">{{ stats.total_listings || 0 }}</div>
            <div class="text-steel-600">总交易数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-green mb-2">{{ stats.active_listings || 0 }}</div>
            <div class="text-steel-600">活跃交易</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-orange mb-2">{{ stats.featured_count || 0 }}</div>
            <div class="text-steel-600">推荐交易</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-600 mb-2">{{ stats.verified_count || 0 }}</div>
            <div class="text-steel-600">已验证</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-600 mb-2">{{ stats.total_views || 0 }}</div>
            <div class="text-steel-600">总浏览量</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-red-600 mb-2">{{ stats.total_inquiries || 0 }}</div>
            <div class="text-steel-600">总询价数</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 交易类型导航 -->
    <section class="py-6 bg-steel-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-wrap gap-4 justify-center">
          <button 
            v-for="type in tradeTypes" 
            :key="type.key"
            @click="filterByType(type.key)"
            :class="[
              'px-6 py-3 rounded-industrial font-medium transition-all duration-200',
              selectedType === type.key 
                ? 'bg-accent-blue text-white shadow-lg' 
                : 'bg-white text-steel-700 hover:bg-steel-100 shadow'
            ]"
          >
            <i :class="type.icon" class="mr-2"></i>
            {{ type.name }}
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
              <label class="block text-sm font-medium text-steel-700 mb-2">产品分类</label>
              <select v-model="filters.category" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部分类</option>
                <option value="显卡">显卡</option>
                <option value="处理器">处理器</option>
                <option value="内存">内存</option>
                <option value="存储">存储设备</option>
                <option value="主板">主板</option>
                <option value="电源">电源</option>
                <option value="散热器">散热器</option>
                <option value="其他">其他</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">制造商</label>
              <select v-model="filters.manufacturer" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部品牌</option>
                <option value="NVIDIA">NVIDIA</option>
                <option value="AMD">AMD</option>
                <option value="Intel">Intel</option>
                <option value="Samsung">Samsung</option>
                <option value="Corsair">Corsair</option>
                <option value="ASUS">ASUS</option>
                <option value="MSI">MSI</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">产品条件</label>
              <select v-model="filters.condition" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部条件</option>
                <option value="new">全新</option>
                <option value="like_new">几乎全新</option>
                <option value="excellent">优秀</option>
                <option value="good">良好</option>
                <option value="fair">一般</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">国家地区</label>
              <select v-model="filters.country" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部地区</option>
                <option value="中国">中国</option>
                <option value="美国">美国</option>
                <option value="日本">日本</option>
                <option value="韩国">韩国</option>
                <option value="德国">德国</option>
                <option value="英国">英国</option>
                <option value="加拿大">加拿大</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">关键词搜索</label>
              <input 
                v-model="filters.keyword" 
                type="text" 
                placeholder="输入产品名称..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                @keyup.enter="searchListings"
              />
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">价格范围</label>
              <div class="flex gap-2">
                <input 
                  v-model="filters.min_price" 
                  type="number" 
                  placeholder="最低价"
                  class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                />
                <input 
                  v-model="filters.max_price" 
                  type="number" 
                  placeholder="最高价"
                  class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                />
              </div>
            </div>
            <div class="flex items-end">
              <div class="flex items-center gap-4">
                <label class="flex items-center">
                  <input type="checkbox" v-model="filters.is_verified" class="mr-2">
                  <span class="text-sm text-steel-700">仅显示已验证</span>
                </label>
                <label class="flex items-center">
                  <input type="checkbox" v-model="filters.is_featured" class="mr-2">
                  <span class="text-sm text-steel-700">仅显示推荐</span>
                </label>
                <label class="flex items-center">
                  <input type="checkbox" v-model="filters.is_urgent" class="mr-2">
                  <span class="text-sm text-steel-700">仅显示紧急</span>
                </label>
              </div>
            </div>
            <div class="flex items-end justify-end gap-4">
              <button @click="resetFilters" class="text-steel-600 hover:text-steel-800">
                重置筛选
              </button>
              <button @click="searchListings" class="btn-primary">
                搜索交易
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 交易列表 -->
    <section class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200 flex justify-between items-center">
            <h3 class="text-lg font-semibold text-steel-800">交易信息列表</h3>
            <div class="flex items-center gap-4">
              <span class="text-sm text-steel-600">排序方式:</span>
              <select v-model="sortBy" @change="searchListings" class="px-3 py-1 border border-steel-300 rounded text-sm">
                <option value="created_at">最新发布</option>
                <option value="price">价格排序</option>
                <option value="view_count">浏览量</option>
                <option value="inquiry_count">询价数</option>
              </select>
            </div>
          </div>
          
          <div v-if="loading" class="p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-blue mx-auto"></div>
            <p class="mt-4 text-steel-600">加载中...</p>
          </div>
          
          <div v-else-if="listings.length === 0" class="p-8 text-center">
            <p class="text-steel-600">暂无交易信息</p>
          </div>
          
          <div v-else class="divide-y divide-steel-200">
            <div 
              v-for="listing in listings" 
              :key="listing.id"
              class="p-6 hover:bg-steel-50 transition-colors cursor-pointer"
              @click="viewListingDetail(listing)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-3">
                    <h4 class="text-xl font-semibold text-steel-800 hover:text-accent-blue">
                      {{ listing.title }}
                    </h4>
                    <span :class="[
                      'px-2 py-1 text-xs rounded-full font-medium',
                      listing.listing_type === 'sell' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-blue-100 text-blue-800'
                    ]">
                      {{ listing.listing_type === 'sell' ? '出售' : '求购' }}
                    </span>
                    <span v-if="listing.is_featured" class="px-2 py-1 bg-accent-orange text-white text-xs rounded-full">
                      推荐
                    </span>
                    <span v-if="listing.is_verified" class="px-2 py-1 bg-accent-green text-white text-xs rounded-full">
                      已验证
                    </span>
                    <span v-if="listing.is_urgent" class="px-2 py-1 bg-red-500 text-white text-xs rounded-full">
                      紧急
                    </span>
                  </div>
                  
                  <div class="flex items-center gap-4 mb-3">
                    <span class="text-lg font-semibold text-steel-800">{{ listing.product_name }}</span>
                    <span class="text-steel-600">{{ listing.manufacturer }}</span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getConditionColor(listing.condition)
                    ]">
                      {{ getConditionText(listing.condition) }}
                    </span>
                  </div>
                  
                  <div class="flex items-center gap-6 text-sm text-steel-500 mb-3">
                    <div class="flex items-center">
                      <i class="fas fa-dollar-sign mr-1"></i>
                      <span class="font-semibold text-lg text-accent-blue">
                        ${{ listing.price || '面议' }}
                      </span>
                      <span v-if="listing.price_type === 'negotiable'" class="ml-1 text-xs">(可议)</span>
                    </div>
                    <div class="flex items-center">
                      <i class="fas fa-cubes mr-1"></i>
                      <span>数量: {{ listing.quantity }}</span>
                    </div>
                    <div class="flex items-center">
                      <i class="fas fa-map-marker-alt mr-1"></i>
                      <span>{{ listing.country }}{{ listing.city ? ` · ${listing.city}` : '' }}</span>
                    </div>
                    <span>{{ listing.view_count }} 浏览</span>
                    <span>{{ listing.inquiry_count }} 询价</span>
                  </div>
                  
                  <p class="text-steel-600 mb-3 line-clamp-2">
                    {{ listing.description }}
                  </p>
                  
                  <div class="text-sm text-steel-500">
                    <span>发布时间: {{ formatDate(listing.created_at) }}</span>
                    <span class="ml-4">联系人: {{ listing.contact_name || '匿名' }}</span>
                  </div>
                </div>
                
                <div class="ml-6 text-right">
                  <button class="text-accent-blue hover:text-blue-700 mb-2 block">
                    查看详情 →
                  </button>
                  <button class="text-accent-green hover:text-green-700 text-sm mb-1 block">
                    立即询价
                  </button>
                  <button class="text-yellow-600 hover:text-yellow-700 text-sm">
                    收藏交易
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="listings.length > 0" class="px-6 py-4 border-t border-steel-200 flex justify-between items-center">
            <div class="text-sm text-steel-600">
              显示 {{ listings.length }} 条结果
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
const listings = ref([])
const loading = ref(false)
const sortBy = ref('created_at')
const selectedType = ref('')

const filters = ref({
  listing_type: '',
  category: '',
  manufacturer: '',
  condition: '',
  country: '',
  keyword: '',
  min_price: '',
  max_price: '',
  is_verified: false,
  is_featured: false,
  is_urgent: false
})

// 交易类型
const tradeTypes = ref([
  { key: '', name: '全部', icon: 'fas fa-th-large' },
  { key: 'sell', name: '出售信息', icon: 'fas fa-tag' },
  { key: 'buy', name: '求购信息', icon: 'fas fa-search' },
  { key: 'exchange', name: '交换信息', icon: 'fas fa-exchange-alt' }
])

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/marketplace/stats')
    if (response.ok) {
      stats.value = await response.json()
    } else {
      console.error('获取统计数据失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取交易信息列表
const fetchListings = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.listing_type) params.append('listing_type', filters.value.listing_type)
    if (filters.value.category) params.append('category', filters.value.category)
    if (filters.value.manufacturer) params.append('manufacturer', filters.value.manufacturer)
    if (filters.value.condition) params.append('condition', filters.value.condition)
    if (filters.value.country) params.append('country', filters.value.country)
    if (filters.value.keyword) params.append('keyword', filters.value.keyword)
    if (filters.value.min_price) params.append('min_price', filters.value.min_price)
    if (filters.value.max_price) params.append('max_price', filters.value.max_price)
    if (filters.value.is_verified) params.append('is_verified', 'true')
    if (filters.value.is_featured) params.append('is_featured', 'true')
    if (filters.value.is_urgent) params.append('is_urgent', 'true')
    params.append('sort_by', sortBy.value)
    params.append('sort_order', 'desc')
    
    const response = await fetch(`http://localhost:8000/api/v1/marketplace/?${params.toString()}`)
    if (response.ok) {
      listings.value = await response.json()
    } else {
      console.error('获取交易信息失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取交易信息失败:', error)
  } finally {
    loading.value = false
  }
}

// 按类型筛选
const filterByType = (type: string) => {
  selectedType.value = type
  filters.value.listing_type = type
  fetchListings()
}

// 搜索交易信息
const searchListings = () => {
  fetchListings()
}

// 重置筛选
const resetFilters = () => {
  filters.value = {
    listing_type: '',
    category: '',
    manufacturer: '',
    condition: '',
    country: '',
    keyword: '',
    min_price: '',
    max_price: '',
    is_verified: false,
    is_featured: false,
    is_urgent: false
  }
  selectedType.value = ''
  fetchListings()
}

// 加载更多
const loadMore = () => {
  // TODO: 实现分页加载
  console.log('加载更多')
}

// 查看交易详情
const viewListingDetail = (listing: any) => {
  // TODO: 跳转到交易详情页面
  console.log('查看交易详情:', listing)
}

// 工具函数
const getConditionColor = (condition: string) => {
  const colors = {
    'new': 'bg-green-100 text-green-800',
    'like_new': 'bg-blue-100 text-blue-800',
    'excellent': 'bg-purple-100 text-purple-800',
    'good': 'bg-yellow-100 text-yellow-800',
    'fair': 'bg-orange-100 text-orange-800',
    'poor': 'bg-red-100 text-red-800'
  }
  return colors[condition] || 'bg-gray-100 text-gray-800'
}

const getConditionText = (condition: string) => {
  const texts = {
    'new': '全新',
    'like_new': '几乎全新',
    'excellent': '优秀',
    'good': '良好',
    'fair': '一般',
    'poor': '较差'
  }
  return texts[condition] || condition
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  fetchListings()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
