<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 返回按钮 -->
    <section class="py-4 bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <button @click="goBack" class="flex items-center text-steel-600 hover:text-accent-blue">
          <i class="fas fa-arrow-left mr-2"></i>
          返回社区
        </button>
      </div>
    </section>

    <!-- 帖子详情 -->
    <section class="py-8">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-blue mx-auto"></div>
          <p class="mt-4 text-steel-600">加载中...</p>
        </div>

        <div v-else-if="post" class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <!-- 帖子头部 -->
          <div class="px-6 py-6 border-b border-steel-200">
            <div class="flex items-center gap-3 mb-4">
              <h1 class="text-2xl font-bold text-steel-800">{{ post.title }}</h1>
              <span :class="['px-2 py-1 text-xs rounded-full font-medium', getTypeColor(post.post_type)]">
                {{ getTypeText(post.post_type) }}
              </span>
              <span :class="['px-2 py-1 text-xs rounded-full font-medium', getPriorityColor(post.priority)]">
                {{ getPriorityText(post.priority) }}
              </span>
              <span v-if="post.is_featured" class="px-2 py-1 bg-accent-orange text-white text-xs rounded-full">
                推荐
              </span>
              <span v-if="post.is_official" class="px-2 py-1 bg-accent-blue text-white text-xs rounded-full">
                官方
              </span>
            </div>

            <div class="flex items-center justify-between text-sm text-steel-500 mb-4">
              <div class="flex items-center gap-6">
                <span>发布时间: {{ formatDate(post.created_at) }}</span>
                <span>最后活跃: {{ formatDate(post.last_activity_at) }}</span>
              </div>
              <div class="flex items-center gap-4">
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
              </div>
            </div>

            <p v-if="post.summary" class="text-steel-600 bg-steel-50 p-4 rounded-industrial">
              {{ post.summary }}
            </p>
          </div>

          <!-- 帖子内容 -->
          <div class="px-6 py-6">
            <div class="prose max-w-none" v-html="formatContent(post.content)"></div>
          </div>

          <!-- 操作按钮 -->
          <div class="px-6 py-4 border-t border-steel-200 flex justify-between items-center">
            <div class="flex gap-4">
              <button @click="toggleLike" :class="[
                'flex items-center px-4 py-2 rounded-industrial transition-colors',
                isLiked ? 'bg-accent-blue text-white' : 'bg-steel-100 text-steel-700 hover:bg-steel-200'
              ]">
                <i class="fas fa-thumbs-up mr-2"></i>
                {{ isLiked ? '已点赞' : '点赞' }} ({{ post.like_count }})
              </button>
              <button @click="toggleFavorite" :class="[
                'flex items-center px-4 py-2 rounded-industrial transition-colors',
                isFavorited ? 'bg-accent-orange text-white' : 'bg-steel-100 text-steel-700 hover:bg-steel-200'
              ]">
                <i class="fas fa-star mr-2"></i>
                {{ isFavorited ? '已收藏' : '收藏' }}
              </button>
              <button class="flex items-center px-4 py-2 bg-steel-100 text-steel-700 hover:bg-steel-200 rounded-industrial transition-colors">
                <i class="fas fa-share mr-2"></i>
                分享
              </button>
            </div>
            <button class="text-steel-500 hover:text-steel-700">
              <i class="fas fa-flag mr-1"></i>
              举报
            </button>
          </div>
        </div>

        <!-- 评论区 -->
        <div class="mt-8 bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200">
            <h3 class="text-lg font-semibold text-steel-800">评论 ({{ comments.length }})</h3>
          </div>

          <!-- 发表评论 -->
          <div class="px-6 py-4 border-b border-steel-200">
            <textarea 
              v-model="newComment" 
              placeholder="写下你的评论..."
              class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue resize-none"
              rows="3"
            ></textarea>
            <div class="mt-3 flex justify-end">
              <button @click="submitComment" :disabled="!newComment.trim()" class="btn-primary">
                发表评论
              </button>
            </div>
          </div>

          <!-- 评论列表 -->
          <div class="divide-y divide-steel-200">
            <div v-for="comment in comments" :key="comment.id" class="px-6 py-4">
              <div class="flex items-start gap-3">
                <div class="w-8 h-8 bg-accent-blue rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">{{ comment.author_name?.[0] || 'U' }}</span>
                </div>
                <div class="flex-1">
                  <div class="flex items-center gap-2 mb-2">
                    <span class="font-medium text-steel-800">{{ comment.author_name || '匿名用户' }}</span>
                    <span class="text-sm text-steel-500">{{ formatDate(comment.created_at) }}</span>
                  </div>
                  <p class="text-steel-700">{{ comment.content }}</p>
                  <div class="mt-2 flex items-center gap-4 text-sm text-steel-500">
                    <button class="hover:text-accent-blue">
                      <i class="fas fa-thumbs-up mr-1"></i>
                      点赞 ({{ comment.like_count || 0 }})
                    </button>
                    <button class="hover:text-accent-blue">
                      <i class="fas fa-reply mr-1"></i>
                      回复
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="comments.length === 0" class="px-6 py-8 text-center text-steel-500">
            暂无评论，快来发表第一条评论吧！
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 响应式数据
const post = ref(null)
const comments = ref([])
const loading = ref(false)
const newComment = ref('')
const isLiked = ref(false)
const isFavorited = ref(false)

// 获取帖子详情
const fetchPost = async () => {
  loading.value = true
  try {
    const response = await fetch(`http://localhost:8001/api/v1/community/${route.params.id}`)
    if (response.ok) {
      post.value = await response.json()
    } else {
      console.error('获取帖子详情失败:', response.status)
    }
  } catch (error) {
    console.error('获取帖子详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取评论列表
const fetchComments = async () => {
  try {
    const response = await fetch(`http://localhost:8001/api/v1/community/${route.params.id}/comments`)
    if (response.ok) {
      comments.value = await response.json()
    }
  } catch (error) {
    console.error('获取评论失败:', error)
  }
}

// 发表评论
const submitComment = async () => {
  if (!newComment.value.trim()) return
  
  try {
    const response = await fetch(`http://localhost:8001/api/v1/community/${route.params.id}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: newComment.value.trim()
      })
    })
    
    if (response.ok) {
      newComment.value = ''
      fetchComments()
    }
  } catch (error) {
    console.error('发表评论失败:', error)
  }
}

// 点赞/取消点赞
const toggleLike = () => {
  isLiked.value = !isLiked.value
  if (isLiked.value) {
    post.value.like_count++
  } else {
    post.value.like_count--
  }
}

// 收藏/取消收藏
const toggleFavorite = () => {
  isFavorited.value = !isFavorited.value
}

// 返回社区
const goBack = () => {
  router.push('/community')
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
  return date.toLocaleString('zh-CN')
}

const formatContent = (content: string) => {
  // 简单的 Markdown 转 HTML
  return content
    .replace(/\n/g, '<br>')
    .replace(/## (.*)/g, '<h2 class="text-xl font-semibold mt-6 mb-3">$1</h2>')
    .replace(/# (.*)/g, '<h1 class="text-2xl font-bold mt-6 mb-4">$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPost()
  fetchComments()
})
</script>

<style scoped>
.prose {
  line-height: 1.7;
}

.prose h1, .prose h2, .prose h3 {
  color: #374151;
}

.prose p {
  margin-bottom: 1rem;
}
</style>
