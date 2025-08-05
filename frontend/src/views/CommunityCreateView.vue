<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部 -->
    <section class="py-4 bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between">
          <button @click="goBack" class="flex items-center text-steel-600 hover:text-accent-blue">
            <i class="fas fa-arrow-left mr-2"></i>
            返回社区
          </button>
          <h1 class="text-xl font-semibold text-steel-800">发布新帖子</h1>
          <div></div>
        </div>
      </div>
    </section>

    <!-- 发布表单 -->
    <section class="py-8">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-industrial shadow-lg overflow-hidden">
          <form @submit.prevent="submitPost" class="p-6 space-y-6">
            <!-- 基本信息 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-steel-700 mb-2">帖子类型 *</label>
                <select v-model="form.post_type" required class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                  <option value="">请选择类型</option>
                  <option value="discussion">讨论</option>
                  <option value="question">问题</option>
                  <option value="experience">经验分享</option>
                  <option value="news">资讯</option>
                  <option value="policy">政策解读</option>
                  <option value="technical">技术交流</option>
                  <option value="market">市场分析</option>
                  <option value="cooperation">合作对接</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-steel-700 mb-2">优先级</label>
                <select v-model="form.priority" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                  <option value="normal">普通</option>
                  <option value="high">高</option>
                  <option value="urgent">紧急</option>
                  <option value="low">低</option>
                </select>
              </div>
            </div>

            <!-- 标题 -->
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">标题 *</label>
              <input 
                v-model="form.title" 
                type="text" 
                required
                placeholder="请输入帖子标题..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
              />
            </div>

            <!-- 摘要 -->
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">摘要</label>
              <textarea 
                v-model="form.summary" 
                placeholder="简要描述帖子内容..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue resize-none"
                rows="2"
              ></textarea>
            </div>

            <!-- 内容 -->
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">内容 *</label>
              <textarea 
                v-model="form.content" 
                required
                placeholder="请输入帖子内容，支持 Markdown 格式..."
                class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue resize-none"
                rows="12"
              ></textarea>
              <p class="mt-1 text-sm text-steel-500">支持 Markdown 格式，如 **粗体**、*斜体*、## 标题 等</p>
            </div>

            <!-- 标签和关键词 -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-steel-700 mb-2">标签</label>
                <input 
                  v-model="tagsInput" 
                  type="text" 
                  placeholder="输入标签，用逗号分隔..."
                  class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                />
                <p class="mt-1 text-sm text-steel-500">例如：半导体,技术,讨论</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-steel-700 mb-2">关键词</label>
                <input 
                  v-model="form.keywords" 
                  type="text" 
                  placeholder="输入关键词，用逗号分隔..."
                  class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue"
                />
              </div>
            </div>

            <!-- 分类 -->
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-2">分类</label>
              <select v-model="form.category_id" class="w-full px-3 py-2 border border-steel-300 rounded-industrial focus:outline-none focus:ring-2 focus:ring-accent-blue">
                <option value="">请选择分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <!-- 特殊标记 -->
            <div>
              <label class="block text-sm font-medium text-steel-700 mb-3">特殊标记</label>
              <div class="flex flex-wrap gap-4">
                <label class="flex items-center">
                  <input type="checkbox" v-model="form.is_urgent" class="mr-2">
                  <span class="text-sm text-steel-700">紧急帖子</span>
                </label>
                <label class="flex items-center">
                  <input type="checkbox" v-model="form.is_featured" class="mr-2">
                  <span class="text-sm text-steel-700">推荐帖子</span>
                </label>
                <label class="flex items-center">
                  <input type="checkbox" v-model="form.is_official" class="mr-2">
                  <span class="text-sm text-steel-700">官方帖子</span>
                </label>
              </div>
            </div>

            <!-- 提交按钮 -->
            <div class="flex justify-end gap-4 pt-6 border-t border-steel-200">
              <button type="button" @click="saveDraft" class="btn-secondary">
                保存草稿
              </button>
              <button type="submit" :disabled="submitting" class="btn-primary">
                <span v-if="submitting">发布中...</span>
                <span v-else>发布帖子</span>
              </button>
            </div>
          </form>
        </div>

        <!-- 预览区域 -->
        <div v-if="form.content" class="mt-8 bg-white rounded-industrial shadow-lg overflow-hidden">
          <div class="px-6 py-4 border-b border-steel-200">
            <h3 class="text-lg font-semibold text-steel-800">预览</h3>
          </div>
          <div class="px-6 py-6">
            <h2 class="text-xl font-bold text-steel-800 mb-4">{{ form.title || '帖子标题' }}</h2>
            <p v-if="form.summary" class="text-steel-600 bg-steel-50 p-4 rounded-industrial mb-4">
              {{ form.summary }}
            </p>
            <div class="prose max-w-none" v-html="formatContent(form.content)"></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const submitting = ref(false)
const categories = ref([])
const tagsInput = ref('')

const form = ref({
  title: '',
  content: '',
  summary: '',
  post_type: '',
  priority: 'normal',
  category_id: '',
  keywords: '',
  is_urgent: false,
  is_featured: false,
  is_official: false
})

// 获取分类列表
const fetchCategories = async () => {
  try {
    const response = await fetch('http://localhost:8001/api/v1/community/categories')
    if (response.ok) {
      categories.value = await response.json()
    }
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 提交帖子
const submitPost = async () => {
  submitting.value = true
  try {
    const postData = {
      ...form.value,
      tags: tagsInput.value ? JSON.stringify(tagsInput.value.split(',').map(tag => tag.trim())) : null
    }

    const response = await fetch('http://localhost:8001/api/v1/community/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData)
    })

    if (response.ok) {
      const result = await response.json()
      router.push(`/community/${result.id}`)
    } else {
      console.error('发布失败:', response.status)
      alert('发布失败，请重试')
    }
  } catch (error) {
    console.error('发布失败:', error)
    alert('发布失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 保存草稿
const saveDraft = () => {
  localStorage.setItem('community_draft', JSON.stringify({
    ...form.value,
    tags: tagsInput.value
  }))
  alert('草稿已保存')
}

// 返回社区
const goBack = () => {
  router.push('/community')
}

// 格式化内容
const formatContent = (content: string) => {
  return content
    .replace(/\n/g, '<br>')
    .replace(/## (.*)/g, '<h2 class="text-xl font-semibold mt-6 mb-3">$1</h2>')
    .replace(/# (.*)/g, '<h1 class="text-2xl font-bold mt-6 mb-4">$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
}

// 组件挂载时加载数据
onMounted(() => {
  fetchCategories()
  
  // 加载草稿
  const draft = localStorage.getItem('community_draft')
  if (draft) {
    try {
      const draftData = JSON.parse(draft)
      form.value = { ...form.value, ...draftData }
      tagsInput.value = draftData.tags || ''
    } catch (error) {
      console.error('加载草稿失败:', error)
    }
  }
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
