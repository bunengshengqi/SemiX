<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold mb-4">
              市场情报
            </h1>
            <p class="text-xl text-steel-200 mb-6 lg:mb-0">
              实时掌握半导体市场动态，洞察行业发展趋势
            </p>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <button class="btn-primary">
              订阅情报
            </button>
            <button class="btn-secondary bg-transparent border-2 border-white text-white hover:bg-white hover:text-steel-800">
              定制报告
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
            <div class="text-3xl font-bold text-accent-blue mb-2">{{ stats.total_intelligence || 0 }}</div>
            <div class="text-steel-600">总情报数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-green mb-2">{{ stats.featured_count || 0 }}</div>
            <div class="text-steel-600">精选情报</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-orange mb-2">{{ stats.trending_count || 0 }}</div>
            <div class="text-steel-600">热门情报</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-600 mb-2">{{ stats.premium_count || 0 }}</div>
            <div class="text-steel-600">付费内容</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-600 mb-2">{{ stats.total_views || 0 }}</div>
            <div class="text-steel-600">总浏览量</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-red-600 mb-2">{{ stats.avg_quality_score || 0 }}</div>
            <div class="text-steel-600">平均评分</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 快速导航 -->
    <section class="py-6 bg-steel-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-wrap gap-4 justify-center">
          <button 
            v-for="category in quickCategories" 
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
              <label class="block text-sm font-medium text-steel-700 mb-2">情报类型</label>
              <select v-model="filters.intelligence_type" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部类型</option>
                <option value="market_trend">市场趋势</option>
                <option value="price_analysis">价格分析</option>
                <option value="supply_chain">供应链情报</option>
                <option value="technology_trend">技术趋势</option>
                <option value="competitor_analysis">竞争对手分析</option>
                <option value="industry_news">行业新闻</option>
                <option value="policy_impact">政策影响</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">优先级</label>
              <select v-model="filters.priority" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部优先级</option>
                <option value="critical">紧急</option>
                <option value="high">高</option>
                <option value="medium">中</option>
                <option value="low">低</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">地区</label>
              <select v-model="filters.region" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部地区</option>
                <option value="global">全球</option>
                <option value="asia_pacific">亚太</option>
                <option value="china">中国</option>
                <option value="japan">日本</option>
                <option value="south_korea">韩国</option>
                <option value="taiwan">台湾省</option>
                <option value="southeast_asia">东南亚</option>
                <option value="north_america">北美</option>
                <option value="europe">欧洲</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">作者</label>
              <input 
                v-model="filters.author" 
                type="text" 
                placeholder="输入作者姓名..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">关键词搜索</label>
              <input 
                v-model="filters.keyword" 
                type="text" 
                placeholder="输入关键词..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                @keyup.enter="searchIntelligence"
              />
            </div>
          </div>
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-4">
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_featured" class="mr-2">
                <span class="text-sm text-steel-700">仅显示精选</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_trending" class="mr-2">
                <span class="text-sm text-steel-700">仅显示热门</span>
              </label>
            </div>
            <div class="flex gap-4">
              <button @click="resetFilters" class="text-steel-600 hover:text-steel-800">
                重置筛选
              </button>
              <button @click="searchIntelligence" class="btn-primary">
                搜索情报
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 情报列表 -->
    <section class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200 flex justify-between items-center">
            <h3 class="text-lg font-semibold text-steel-800">市场情报列表</h3>
            <div class="flex items-center gap-4">
              <span class="text-sm text-steel-600">排序方式:</span>
              <select v-model="sortBy" @change="searchIntelligence" class="px-3 py-1 border border-steel-300 rounded text-sm">
                <option value="created_at">最新发布</option>
                <option value="view_count">浏览量</option>
                <option value="quality_score">质量评分</option>
                <option value="relevance_score">相关性</option>
                <option value="timeliness_score">时效性</option>
              </select>
            </div>
          </div>
          
          <div v-if="loading" class="p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-blue mx-auto"></div>
            <p class="mt-4 text-steel-600">加载中...</p>
          </div>
          
          <div v-else-if="intelligence.length === 0" class="p-8 text-center">
            <p class="text-steel-600">暂无市场情报数据</p>
          </div>
          
          <div v-else class="divide-y divide-steel-200">
            <div 
              v-for="item in intelligence" 
              :key="item.id"
              class="p-6 hover:bg-steel-50 transition-colors cursor-pointer"
              @click="viewIntelligenceDetail(item)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-3">
                    <h4 class="text-xl font-semibold text-steel-800 hover:text-accent-blue">
                      {{ item.title }}
                    </h4>
                    <span v-if="item.is_featured" class="px-2 py-1 bg-accent-orange text-white text-xs rounded-full">
                      精选
                    </span>
                    <span v-if="item.is_trending" class="px-2 py-1 bg-accent-green text-white text-xs rounded-full">
                      热门
                    </span>
                    <span v-if="item.is_premium" class="px-2 py-1 bg-purple-600 text-white text-xs rounded-full">
                      付费
                    </span>
                  </div>
                  
                  <p v-if="item.subtitle" class="text-steel-600 mb-2 font-medium">
                    {{ item.subtitle }}
                  </p>
                  
                  <div class="flex items-center gap-4 mb-3">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getTypeColor(item.intelligence_type)
                    ]">
                      {{ getTypeText(item.intelligence_type) }}
                    </span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getPriorityColor(item.priority)
                    ]">
                      {{ getPriorityText(item.priority) }}
                    </span>
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      getRegionColor(item.region)
                    ]">
                      {{ getRegionText(item.region) }}
                    </span>
                  </div>
                  
                  <p class="text-steel-600 mb-3 line-clamp-2">
                    {{ item.summary }}
                  </p>
                  
                  <div class="flex items-center gap-6 text-sm text-steel-500 mb-3">
                    <div class="flex items-center">
                      <span class="text-yellow-400 mr-1">★</span>
                      <span>{{ item.quality_score }}/5.0</span>
                    </div>
                    <span>{{ item.view_count }} 浏览</span>
                    <span>{{ item.like_count }} 点赞</span>
                    <span>{{ item.comment_count }} 评论</span>
                    <span>{{ formatDate(item.report_date) }}</span>
                  </div>
                  
                  <div class="text-sm text-steel-600">
                    <span class="font-medium">作者:</span> {{ item.author || '未知' }}
                    <span class="ml-4 font-medium">机构:</span> {{ item.organization || '未知' }}
                  </div>
                </div>
                
                <div class="ml-6 text-right">
                  <button class="text-accent-blue hover:text-blue-700 mb-2 block">
                    查看详情 →
                  </button>
                  <button class="text-accent-green hover:text-green-700 text-sm">
                    收藏情报
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="intelligence.length > 0" class="px-6 py-4 border-t border-steel-200 flex justify-between items-center">
            <div class="text-sm text-steel-600">
              显示 {{ intelligence.length }} 条结果
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
const intelligence = ref([])
const loading = ref(false)
const sortBy = ref('created_at')
const selectedCategory = ref('')

const filters = ref({
  intelligence_type: '',
  priority: '',
  region: '',
  author: '',
  keyword: '',
  is_featured: false,
  is_trending: false
})

// 快速分类
const quickCategories = ref([
  { key: '', name: '全部', icon: 'fas fa-th-large' },
  { key: 'market_trend', name: '市场趋势', icon: 'fas fa-chart-line' },
  { key: 'price_analysis', name: '价格分析', icon: 'fas fa-dollar-sign' },
  { key: 'technology_trend', name: '技术趋势', icon: 'fas fa-microchip' },
  { key: 'competitor_analysis', name: '竞争分析', icon: 'fas fa-users' },
  { key: 'policy_impact', name: '政策影响', icon: 'fas fa-gavel' }
])

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/market/stats')
    if (response.ok) {
      stats.value = await response.json()
    } else {
      console.error('获取统计数据失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取市场情报列表
const fetchIntelligence = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.intelligence_type) params.append('intelligence_type', filters.value.intelligence_type)
    if (filters.value.priority) params.append('priority', filters.value.priority)
    if (filters.value.region) params.append('region', filters.value.region)
    if (filters.value.author) params.append('author', filters.value.author)
    if (filters.value.keyword) params.append('keyword', filters.value.keyword)
    if (filters.value.is_featured) params.append('is_featured', 'true')
    if (filters.value.is_trending) params.append('is_trending', 'true')
    params.append('sort_by', sortBy.value)
    params.append('sort_order', 'desc')
    
    const response = await fetch(`http://localhost:8000/api/v1/market/?${params.toString()}`)
    if (response.ok) {
      intelligence.value = await response.json()
    } else {
      console.error('获取市场情报失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取市场情报失败:', error)
  } finally {
    loading.value = false
  }
}

// 按分类筛选
const filterByCategory = (category: string) => {
  selectedCategory.value = category
  filters.value.intelligence_type = category
  fetchIntelligence()
}

// 搜索情报
const searchIntelligence = () => {
  fetchIntelligence()
}

// 重置筛选
const resetFilters = () => {
  filters.value = {
    intelligence_type: '',
    priority: '',
    region: '',
    author: '',
    keyword: '',
    is_featured: false,
    is_trending: false
  }
  selectedCategory.value = ''
  fetchIntelligence()
}

// 加载更多
const loadMore = () => {
  // TODO: 实现分页加载
  console.log('加载更多')
}

// 查看情报详情
const viewIntelligenceDetail = (item: any) => {
  // TODO: 跳转到情报详情页面
  console.log('查看情报详情:', item)
}

// 工具函数
const getTypeColor = (type: string) => {
  const colors = {
    'market_trend': 'bg-blue-100 text-blue-800',
    'price_analysis': 'bg-green-100 text-green-800',
    'supply_chain': 'bg-yellow-100 text-yellow-800',
    'technology_trend': 'bg-purple-100 text-purple-800',
    'competitor_analysis': 'bg-red-100 text-red-800',
    'industry_news': 'bg-indigo-100 text-indigo-800',
    'policy_impact': 'bg-orange-100 text-orange-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getTypeText = (type: string) => {
  const texts = {
    'market_trend': '市场趋势',
    'price_analysis': '价格分析',
    'supply_chain': '供应链情报',
    'technology_trend': '技术趋势',
    'competitor_analysis': '竞争对手分析',
    'industry_news': '行业新闻',
    'policy_impact': '政策影响'
  }
  return texts[type] || type
}

const getPriorityColor = (priority: string) => {
  const colors = {
    'critical': 'bg-red-100 text-red-800',
    'high': 'bg-orange-100 text-orange-800',
    'medium': 'bg-yellow-100 text-yellow-800',
    'low': 'bg-green-100 text-green-800'
  }
  return colors[priority] || 'bg-gray-100 text-gray-800'
}

const getPriorityText = (priority: string) => {
  const texts = {
    'critical': '紧急',
    'high': '高',
    'medium': '中',
    'low': '低'
  }
  return texts[priority] || priority
}

const getRegionColor = (region: string) => {
  const colors = {
    'global': 'bg-blue-100 text-blue-800',
    'asia_pacific': 'bg-green-100 text-green-800',
    'china': 'bg-red-100 text-red-800',
    'japan': 'bg-purple-100 text-purple-800',
    'south_korea': 'bg-indigo-100 text-indigo-800',
    'taiwan': 'bg-orange-100 text-orange-800',
    'southeast_asia': 'bg-yellow-100 text-yellow-800',
    'north_america': 'bg-pink-100 text-pink-800',
    'europe': 'bg-teal-100 text-teal-800'
  }
  return colors[region] || 'bg-gray-100 text-gray-800'
}

const getRegionText = (region: string) => {
  const texts = {
    'global': '全球',
    'asia_pacific': '亚太',
    'china': '中国',
    'japan': '日本',
    'south_korea': '韩国',
    'taiwan': '台湾省',
    'southeast_asia': '东南亚',
    'north_america': '北美',
    'europe': '欧洲'
  }
  return texts[region] || region
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  fetchIntelligence()
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
