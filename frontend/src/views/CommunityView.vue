<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">
            讨论社区
          </h1>
          <p class="text-xl text-steel-200 mb-8">
            半导体出海专业交流平台，分享经验，解决问题，共同成长
          </p>
          <div class="flex justify-center space-x-4">
            <button @click="router.push('/community/create')" class="btn-primary">
              发布帖子
            </button>
            <button class="btn-secondary bg-transparent border-2 border-white text-white hover:bg-white hover:text-steel-800">
              浏览话题
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 社区统计 -->
    <section class="py-8 bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-6 gap-6">
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-blue mb-2">{{ stats.total_posts || 0 }}</div>
            <div class="text-steel-600">总帖子数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-green mb-2">{{ stats.active_posts || 0 }}</div>
            <div class="text-steel-600">活跃帖子</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-accent-orange mb-2">{{ stats.featured_count || 0 }}</div>
            <div class="text-steel-600">推荐帖子</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-600 mb-2">{{ stats.total_views || 0 }}</div>
            <div class="text-steel-600">总浏览量</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-yellow-600 mb-2">{{ stats.total_comments || 0 }}</div>
            <div class="text-steel-600">总评论数</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-red-600 mb-2">{{ stats.total_likes || 0 }}</div>
            <div class="text-steel-600">总点赞数</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 帖子类型导航 -->
    <section class="py-6 bg-steel-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-wrap gap-4 justify-center">
          <button 
            v-for="type in postTypes" 
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
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">优先级</label>
              <select v-model="filters.priority" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部优先级</option>
                <option value="urgent">紧急</option>
                <option value="high">高</option>
                <option value="normal">普通</option>
                <option value="low">低</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">分类</label>
              <select v-model="filters.category_id" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">全部分类</option>
                <option value="1">热门话题</option>
                <option value="2">问答专区</option>
                <option value="3">经验分享</option>
                <option value="4">政策解读</option>
                <option value="5">技术交流</option>
                <option value="6">市场分析</option>
                <option value="7">供需对接</option>
                <option value="8">新闻资讯</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">关键词搜索</label>
              <input 
                v-model="filters.keyword" 
                type="text" 
                placeholder="输入关键词..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                @keyup.enter="searchPosts"
              />
            </div>
            <div class="flex items-end">
              <div class="flex items-center gap-4">
                <label class="flex items-center">
                  <input type="checkbox" v-model="filters.is_featured" class="mr-2">
                  <span class="text-sm text-steel-700">仅显示推荐</span>
                </label>
                <label class="flex items-center">
                  <input type="checkbox" v-model="filters.is_official" class="mr-2">
                  <span class="text-sm text-steel-700">仅显示官方</span>
                </label>
              </div>
            </div>
          </div>
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-4">
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_expert_verified" class="mr-2">
                <span class="text-sm text-steel-700">专家认证</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_hot" class="mr-2">
                <span class="text-sm text-steel-700">热门帖子</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_urgent" class="mr-2">
                <span class="text-sm text-steel-700">紧急帖子</span>
              </label>
              <label class="flex items-center">
                <input type="checkbox" v-model="filters.is_solved" class="mr-2">
                <span class="text-sm text-steel-700">已解决</span>
              </label>
            </div>
            <div class="flex gap-4">
              <button @click="resetFilters" class="text-steel-600 hover:text-steel-800">
                重置筛选
              </button>
              <button @click="searchPosts" class="btn-primary">
                搜索帖子
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 帖子列表 -->
    <section class="py-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200 flex justify-between items-center">
            <h3 class="text-lg font-semibold text-steel-800">社区帖子</h3>
            <div class="flex items-center gap-4">
              <span class="text-sm text-steel-600">排序方式:</span>
              <select v-model="sortBy" @change="searchPosts" class="px-3 py-1 border border-steel-300 rounded text-sm">
                <option value="last_activity_at">最新活跃</option>
                <option value="created_at">最新发布</option>
                <option value="view_count">浏览量</option>
                <option value="like_count">点赞数</option>
                <option value="comment_count">评论数</option>
              </select>
            </div>
          </div>
          
          <div v-if="loading" class="p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-blue mx-auto"></div>
            <p class="mt-4 text-steel-600">加载中...</p>
          </div>
          
          <div v-else-if="posts.length === 0" class="p-8 text-center">
            <p class="text-steel-600">暂无帖子数据</p>
          </div>
          
          <div v-else class="divide-y divide-steel-200">
            <div 
              v-for="post in posts" 
              :key="post.id"
              class="p-6 hover:bg-steel-50 transition-colors cursor-pointer"
              @click="viewPostDetail(post)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-3">
                    <h4 class="text-xl font-semibold text-steel-800 hover:text-accent-blue">
                      {{ post.title }}
                    </h4>
                    <span :class="[
                      'px-2 py-1 text-xs rounded-full font-medium',
                      getTypeColor(post.post_type)
                    ]">
                      {{ getTypeText(post.post_type) }}
                    </span>
                    <span :class="[
                      'px-2 py-1 text-xs rounded-full font-medium',
                      getPriorityColor(post.priority)
                    ]">
                      {{ getPriorityText(post.priority) }}
                    </span>
                    <span v-if="post.is_featured" class="px-2 py-1 bg-accent-orange text-white text-xs rounded-full">
                      推荐
                    </span>
                    <span v-if="post.is_official" class="px-2 py-1 bg-accent-blue text-white text-xs rounded-full">
                      官方
                    </span>
                    <span v-if="post.is_expert_verified" class="px-2 py-1 bg-accent-green text-white text-xs rounded-full">
                      专家认证
                    </span>
                    <span v-if="post.is_hot" class="px-2 py-1 bg-red-500 text-white text-xs rounded-full">
                      热门
                    </span>
                    <span v-if="post.is_urgent" class="px-2 py-1 bg-yellow-500 text-white text-xs rounded-full">
                      紧急
                    </span>
                    <span v-if="post.is_solved" class="px-2 py-1 bg-green-500 text-white text-xs rounded-full">
                      已解决
                    </span>
                  </div>
                  
                  <p v-if="post.summary" class="text-steel-600 mb-3 line-clamp-2">
                    {{ post.summary }}
                  </p>
                  
                  <div class="flex items-center gap-6 text-sm text-steel-500 mb-3">
                    <div class="flex items-center">
                      <i class="fas fa-eye mr-1"></i>
                      <span>{{ post.view_count }} 浏览</span>
                    </div>
                    <div class="flex items-center">
                      <i class="fas fa-thumbs-up mr-1"></i>
                      <span>{{ post.like_count }} 点赞</span>
                    </div>
                    <div class="flex items-center">
                      <i class="fas fa-comments mr-1"></i>
                      <span>{{ post.comment_count }} 评论</span>
                    </div>
                    <div class="flex items-center">
                      <i class="fas fa-star mr-1"></i>
                      <span>{{ post.favorite_count }} 收藏</span>
                    </div>
                  </div>
                  
                  <div class="text-sm text-steel-500">
                    <span>发布时间: {{ formatDate(post.created_at) }}</span>
                    <span class="ml-4">最后活跃: {{ formatDate(post.last_activity_at) }}</span>
                  </div>
                </div>
                
                <div class="ml-6 text-right">
                  <button class="text-accent-blue hover:text-blue-700 mb-2 block">
                    查看详情 →
                  </button>
                  <button class="text-accent-green hover:text-green-700 text-sm mb-1 block">
                    参与讨论
                  </button>
                  <button class="text-yellow-600 hover:text-yellow-700 text-sm">
                    收藏帖子
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 分页 -->
          <div v-if="posts.length > 0" class="px-6 py-4 border-t border-steel-200 flex justify-between items-center">
            <div class="text-sm text-steel-600">
              显示 {{ posts.length }} 条结果
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
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const stats = ref({})
const posts = ref([])
const loading = ref(false)
const sortBy = ref('last_activity_at')
const selectedType = ref('')

const filters = ref({
  post_type: '',
  priority: '',
  category_id: '',
  keyword: '',
  is_featured: false,
  is_official: false,
  is_expert_verified: false,
  is_hot: false,
  is_urgent: false,
  is_solved: false
})

// 帖子类型
const postTypes = ref([
  { key: '', name: '全部', icon: 'fas fa-th-large' },
  { key: 'discussion', name: '讨论', icon: 'fas fa-comments' },
  { key: 'question', name: '问题', icon: 'fas fa-question-circle' },
  { key: 'experience', name: '经验', icon: 'fas fa-lightbulb' },
  { key: 'news', name: '资讯', icon: 'fas fa-newspaper' },
  { key: 'policy', name: '政策', icon: 'fas fa-gavel' },
  { key: 'technical', name: '技术', icon: 'fas fa-cogs' },
  { key: 'market', name: '市场', icon: 'fas fa-chart-line' },
  { key: 'cooperation', name: '合作', icon: 'fas fa-handshake' }
])

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await fetch('http://localhost:8001/api/v1/community/stats')
    if (response.ok) {
      stats.value = await response.json()
    } else {
      console.error('获取统计数据失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取帖子列表
const fetchPosts = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.value.post_type) params.append('post_type', filters.value.post_type)
    if (filters.value.priority) params.append('priority', filters.value.priority)
    if (filters.value.category_id) params.append('category_id', filters.value.category_id)
    if (filters.value.keyword) params.append('keyword', filters.value.keyword)
    if (filters.value.is_featured) params.append('is_featured', 'true')
    if (filters.value.is_official) params.append('is_official', 'true')
    if (filters.value.is_expert_verified) params.append('is_expert_verified', 'true')
    if (filters.value.is_hot) params.append('is_hot', 'true')
    if (filters.value.is_urgent) params.append('is_urgent', 'true')
    if (filters.value.is_solved) params.append('is_solved', 'true')
    params.append('sort_by', sortBy.value)
    params.append('sort_order', 'desc')
    
    const response = await fetch(`http://localhost:8001/api/v1/community/?${params.toString()}`)
    if (response.ok) {
      posts.value = await response.json()
    } else {
      console.error('获取帖子失败:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('获取帖子失败:', error)
  } finally {
    loading.value = false
  }
}

// 按类型筛选
const filterByType = (type: string) => {
  selectedType.value = type
  filters.value.post_type = type
  fetchPosts()
}

// 搜索帖子
const searchPosts = () => {
  fetchPosts()
}

// 重置筛选
const resetFilters = () => {
  filters.value = {
    post_type: '',
    priority: '',
    category_id: '',
    keyword: '',
    is_featured: false,
    is_official: false,
    is_expert_verified: false,
    is_hot: false,
    is_urgent: false,
    is_solved: false
  }
  selectedType.value = ''
  fetchPosts()
}

// 加载更多
const loadMore = () => {
  // TODO: 实现分页加载
  console.log('加载更多')
}

// 查看帖子详情
const viewPostDetail = (post: any) => {
  router.push(`/community/${post.id}`)
}

// 工具函数
const getTypeColor = (type: string) => {
  const colors = {
    'discussion': 'bg-blue-100 text-blue-800',
    'question': 'bg-green-100 text-green-800',
    'experience': 'bg-yellow-100 text-yellow-800',
    'news': 'bg-red-100 text-red-800',
    'policy': 'bg-purple-100 text-purple-800',
    'technical': 'bg-indigo-100 text-indigo-800',
    'market': 'bg-pink-100 text-pink-800',
    'cooperation': 'bg-orange-100 text-orange-800'
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
}

const getTypeText = (type: string) => {
  const texts = {
    'discussion': '讨论',
    'question': '问题',
    'experience': '经验',
    'news': '资讯',
    'policy': '政策',
    'technical': '技术',
    'market': '市场',
    'cooperation': '合作'
  }
  return texts[type] || type
}

const getPriorityColor = (priority: string) => {
  const colors = {
    'urgent': 'bg-red-100 text-red-800',
    'high': 'bg-orange-100 text-orange-800',
    'normal': 'bg-blue-100 text-blue-800',
    'low': 'bg-gray-100 text-gray-800'
  }
  return colors[priority] || 'bg-gray-100 text-gray-800'
}

const getPriorityText = (priority: string) => {
  const texts = {
    'urgent': '紧急',
    'high': '高',
    'normal': '普通',
    'low': '低'
  }
  return texts[priority] || priority
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
  fetchPosts()
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
