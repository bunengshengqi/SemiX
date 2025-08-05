<script setup lang="ts">
import { TrendingUp, Globe, Shield, Users } from 'lucide-vue-next'

const scrollToFeatures = () => {
  const featuresSection = document.querySelector('#features-section')
  if (featuresSection) {
    featuresSection.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            <span class="block text-white">半导体出海</span>
            <span class="block text-accent-orange">全链条信息服务</span>
          </h1>
          <p class="text-xl md:text-2xl text-steel-200 mb-8 max-w-3xl mx-auto">
            为半导体企业提供日韩新台政策监控、供应商目录、市场情报、合规工具等一站式出海服务
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <RouterLink to="/register" class="btn-primary text-lg px-8 py-3 text-center">
              免费试用
            </RouterLink>
            <button class="btn-secondary text-lg px-8 py-3 bg-transparent border-2 border-white text-white hover:bg-white hover:text-steel-800" @click="scrollToFeatures">
              查看演示
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 核心功能模块 -->
    <section id="features-section" class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-steel-800 mb-4">核心服务模块</h2>
          <p class="text-steel-600 text-lg">专业、及时、准确的半导体出海信息服务</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <!-- 政策监控 -->
          <div class="card text-center hover:shadow-xl transition-shadow duration-300">
            <div class="w-12 h-12 bg-accent-blue rounded-full flex items-center justify-center mx-auto mb-4">
              <Globe class="h-6 w-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-steel-800 mb-2">政策监控台</h3>
            <p class="text-steel-600 mb-4">日韩新台+国内政策实时对比，政策解读快且准确</p>
            <RouterLink to="/policies" class="text-accent-blue hover:text-blue-600 font-medium">
              了解更多 →
            </RouterLink>
          </div>

          <!-- 供应商目录 -->
          <div class="card text-center hover:shadow-xl transition-shadow duration-300">
            <div class="w-12 h-12 bg-accent-orange rounded-full flex items-center justify-center mx-auto mb-4">
              <Users class="h-6 w-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-steel-800 mb-2">供应商目录</h3>
            <p class="text-steel-600 mb-4">按地区/产品分类的专业数据库，海外资源深度整合</p>
            <RouterLink to="/suppliers" class="text-accent-blue hover:text-blue-600 font-medium">
              了解更多 →
            </RouterLink>
          </div>

          <!-- 市场情报 -->
          <div class="card text-center hover:shadow-xl transition-shadow duration-300">
            <div class="w-12 h-12 bg-accent-green rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingUp class="h-6 w-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-steel-800 mb-2">市场情报</h3>
            <p class="text-steel-600 mb-4">价格指数、需求预测、贸易数据等专业分析</p>
            <RouterLink to="/market" class="text-accent-blue hover:text-blue-600 font-medium">
              了解更多 →
            </RouterLink>
          </div>

          <!-- 合规工具 -->
          <div class="card text-center hover:shadow-xl transition-shadow duration-300">
            <div class="w-12 h-12 bg-accent-red rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield class="h-6 w-6 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-steel-800 mb-2">合规工具</h3>
            <p class="text-steel-600 mb-4">出口许可查询、HS编码对照、税收计算器</p>
            <RouterLink to="/compliance" class="text-accent-blue hover:text-blue-600 font-medium">
              了解更多 →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- 目标市场 -->
    <section class="py-16 bg-industrial-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-steel-800 mb-4">覆盖重点市场</h2>
          <p class="text-steel-600 text-lg">深度整合日韩新台海外资源，本土化国内政策解析</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-industrial shadow-industrial border-l-4 border-accent-blue">
            <h3 class="font-semibold text-steel-800 mb-2">🇯🇵 日本市场</h3>
            <p class="text-steel-600 text-sm">汽车半导体、工业自动化芯片、熊本工厂动态</p>
          </div>
          <div class="bg-white p-6 rounded-industrial shadow-industrial border-l-4 border-accent-orange">
            <h3 class="font-semibold text-steel-800 mb-2">🇰🇷 韩国市场</h3>
            <p class="text-steel-600 text-sm">存储芯片市场、K-半导体带政策、中韩贸易限制</p>
          </div>
          <div class="bg-white p-6 rounded-industrial shadow-industrial border-l-4 border-accent-green">
            <h3 class="font-semibold text-steel-800 mb-2">🇸🇬 新加坡市场</h3>
            <p class="text-steel-600 text-sm">东南亚制造中心、政府投资激励、中转贸易枢纽</p>
          </div>
          <div class="bg-white p-6 rounded-industrial shadow-industrial border-l-4 border-accent-red">
            <h3 class="font-semibold text-steel-800 mb-2">🇹🇼 台湾市场</h3>
            <p class="text-steel-600 text-sm">台积电供应链动态、两岸贸易政策、封测产业链</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
