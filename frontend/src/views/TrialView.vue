<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-accent-orange to-orange-600 text-white py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-6">
            开始免费试用
          </h1>
          <p class="text-xl text-orange-100 mb-8 max-w-3xl mx-auto">
            立即体验SemiX半导体出海信息服务平台，无需信用卡
          </p>
        </div>
      </div>
    </section>

    <!-- 试用套餐选择 -->
    <section class="py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-steel-800 mb-4">选择您的试用方案</h2>
          <p class="text-steel-600 text-lg">根据您的需求选择最适合的试用套餐</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- 基础试用 -->
          <div class="bg-white rounded-industrial shadow-industrial-lg p-8 border-2 border-transparent hover:border-accent-blue transition-all duration-200">
            <div class="text-center mb-6">
              <h3 class="text-2xl font-bold text-steel-800 mb-2">基础试用</h3>
              <div class="text-4xl font-bold text-accent-blue mb-2">免费</div>
              <div class="text-steel-600">7天试用</div>
            </div>
            
            <ul class="space-y-3 mb-8">
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">政策监控基础功能</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">供应商目录查询</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">基础市场数据</span>
              </li>
              <li class="flex items-center">
                <span class="text-steel-400 mr-3">×</span>
                <span class="text-steel-400">高级分析报告</span>
              </li>
              <li class="flex items-center">
                <span class="text-steel-400 mr-3">×</span>
                <span class="text-steel-400">API接口访问</span>
              </li>
            </ul>
            
            <button 
              @click="selectPlan('basic')"
              :class="[
                'w-full py-3 px-6 rounded-industrial font-medium transition-all duration-200',
                selectedPlan === 'basic' 
                  ? 'bg-accent-blue text-white' 
                  : 'bg-steel-100 text-steel-700 hover:bg-steel-200'
              ]"
            >
              {{ selectedPlan === 'basic' ? '已选择' : '选择基础版' }}
            </button>
          </div>

          <!-- 专业试用 -->
          <div class="bg-white rounded-industrial shadow-industrial-lg p-8 border-2 border-accent-orange relative">
            <div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span class="bg-accent-orange text-white px-4 py-1 rounded-full text-sm font-medium">推荐</span>
            </div>
            
            <div class="text-center mb-6">
              <h3 class="text-2xl font-bold text-steel-800 mb-2">专业试用</h3>
              <div class="text-4xl font-bold text-accent-orange mb-2">免费</div>
              <div class="text-steel-600">14天试用</div>
            </div>
            
            <ul class="space-y-3 mb-8">
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">政策监控完整功能</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">供应商目录高级搜索</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">完整市场情报</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">高级分析报告</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">合规工具套件</span>
              </li>
            </ul>
            
            <button 
              @click="selectPlan('professional')"
              :class="[
                'w-full py-3 px-6 rounded-industrial font-medium transition-all duration-200',
                selectedPlan === 'professional' 
                  ? 'bg-accent-orange text-white' 
                  : 'bg-accent-orange text-white hover:bg-orange-600'
              ]"
            >
              {{ selectedPlan === 'professional' ? '已选择' : '选择专业版' }}
            </button>
          </div>

          <!-- 企业试用 -->
          <div class="bg-white rounded-industrial shadow-industrial-lg p-8 border-2 border-transparent hover:border-accent-green transition-all duration-200">
            <div class="text-center mb-6">
              <h3 class="text-2xl font-bold text-steel-800 mb-2">企业试用</h3>
              <div class="text-4xl font-bold text-accent-green mb-2">免费</div>
              <div class="text-steel-600">30天试用</div>
            </div>
            
            <ul class="space-y-3 mb-8">
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">所有功能无限制</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">API接口访问</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">定制化报告</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">专属客户经理</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-500 mr-3">✓</span>
                <span class="text-steel-700">24/7技术支持</span>
              </li>
            </ul>
            
            <button 
              @click="selectPlan('enterprise')"
              :class="[
                'w-full py-3 px-6 rounded-industrial font-medium transition-all duration-200',
                selectedPlan === 'enterprise' 
                  ? 'bg-accent-green text-white' 
                  : 'bg-steel-100 text-steel-700 hover:bg-steel-200'
              ]"
            >
              {{ selectedPlan === 'enterprise' ? '已选择' : '选择企业版' }}
            </button>
          </div>
        </div>

        <!-- 试用流程 -->
        <div class="mt-16">
          <h3 class="text-2xl font-bold text-steel-800 text-center mb-8">开始试用只需3步</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="text-center">
              <div class="w-16 h-16 bg-accent-blue rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl font-bold text-white">1</span>
              </div>
              <h4 class="text-lg font-semibold text-steel-800 mb-2">注册账户</h4>
              <p class="text-steel-600">填写基本信息，无需信用卡</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 bg-accent-orange rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl font-bold text-white">2</span>
              </div>
              <h4 class="text-lg font-semibold text-steel-800 mb-2">选择试用套餐</h4>
              <p class="text-steel-600">根据需求选择合适的试用方案</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 bg-accent-green rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl font-bold text-white">3</span>
              </div>
              <h4 class="text-lg font-semibold text-steel-800 mb-2">立即开始</h4>
              <p class="text-steel-600">马上体验完整功能</p>
            </div>
          </div>
        </div>

        <!-- 行动按钮 -->
        <div class="text-center mt-12">
          <div v-if="selectedPlan" class="mb-6">
            <div class="inline-flex items-center bg-white rounded-industrial shadow-lg px-6 py-3">
              <span class="text-steel-600 mr-2">已选择:</span>
              <span class="font-semibold text-steel-800">
                {{ selectedPlan === 'basic' ? '基础试用' : selectedPlan === 'professional' ? '专业试用' : '企业试用' }}
              </span>
            </div>
          </div>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <RouterLink 
              :to="selectedPlan ? '/register?plan=' + selectedPlan : '/register'" 
              class="btn-primary text-lg px-8 py-3"
            >
              {{ selectedPlan ? '开始' + (selectedPlan === 'basic' ? '基础' : selectedPlan === 'professional' ? '专业' : '企业') + '试用' : '立即注册试用' }}
            </RouterLink>
            <RouterLink to="/demo" class="btn-secondary text-lg px-8 py-3">
              先看产品演示
            </RouterLink>
          </div>
          
          <p class="text-sm text-steel-500 mt-4">
            试用期结束后可随时取消，无任何费用
          </p>
        </div>

        <!-- 常见问题 -->
        <div class="mt-16">
          <h3 class="text-2xl font-bold text-steel-800 text-center mb-8">常见问题</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-white rounded-industrial shadow-lg p-6">
              <h4 class="font-semibold text-steel-800 mb-2">试用期间需要付费吗？</h4>
              <p class="text-steel-600">完全免费，无需提供信用卡信息，试用期结束后不会自动扣费。</p>
            </div>
            <div class="bg-white rounded-industrial shadow-lg p-6">
              <h4 class="font-semibold text-steel-800 mb-2">试用期间可以更换套餐吗？</h4>
              <p class="text-steel-600">可以随时升级到更高级的套餐，享受更多功能和更长的试用期。</p>
            </div>
            <div class="bg-white rounded-industrial shadow-lg p-6">
              <h4 class="font-semibold text-steel-800 mb-2">试用数据会保留吗？</h4>
              <p class="text-steel-600">试用期间的所有数据和设置都会保留，正式订阅后可继续使用。</p>
            </div>
            <div class="bg-white rounded-industrial shadow-lg p-6">
              <h4 class="font-semibold text-steel-800 mb-2">需要技术支持怎么办？</h4>
              <p class="text-steel-600">我们提供邮件和在线客服支持，企业试用用户还享有专属客户经理服务。</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const selectedPlan = ref('professional') // 默认推荐专业版

const selectPlan = (plan: string) => {
  selectedPlan.value = plan
}
</script>
