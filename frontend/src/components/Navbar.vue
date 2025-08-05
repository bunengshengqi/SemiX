<template>
  <nav class="navbar">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo和品牌名 -->
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <div class="w-8 h-8 bg-accent-blue rounded-industrial mr-3 flex items-center justify-center">
              <span class="text-white font-bold text-sm">S</span>
            </div>
            <h1 class="text-xl font-bold text-white">SemiX</h1>
            <span class="ml-2 text-steel-300 text-sm hidden sm:block">半导体出海信息服务平台</span>
          </div>
        </div>

        <!-- 主导航菜单 -->
        <div class="hidden md:flex items-center space-x-8">
          <RouterLink to="/" class="nav-link">首页</RouterLink>
          <div class="relative group">
            <button class="nav-link flex items-center">
              信息服务
              <ChevronDownIcon class="ml-1 h-4 w-4" />
            </button>
            <div class="absolute left-0 mt-2 w-48 bg-white rounded-industrial shadow-industrial-lg border border-steel-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
              <RouterLink to="/policies" class="dropdown-link">政策监控台</RouterLink>
              <RouterLink to="/suppliers" class="dropdown-link">供应商目录</RouterLink>
              <RouterLink to="/market" class="dropdown-link">市场情报</RouterLink>
              <RouterLink to="/compliance" class="dropdown-link">合规工具</RouterLink>
            </div>
          </div>
          <RouterLink to="/community" class="nav-link">讨论社区</RouterLink>
          <RouterLink to="/about" class="nav-link">关于我们</RouterLink>
        </div>

        <!-- 用户操作区 -->
        <div class="flex items-center space-x-4">
          <RouterLink to="/login" class="btn-secondary text-sm">登录</RouterLink>
          <RouterLink to="/register" class="btn-primary text-sm">免费注册</RouterLink>
        </div>

        <!-- 移动端菜单按钮 -->
        <div class="md:hidden flex items-center">
          <button class="text-white hover:text-steel-300">
            <MenuIcon class="h-6 w-6" />
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ChevronDown as ChevronDownIcon, Menu as MenuIcon } from 'lucide-vue-next'
</script>

<style scoped>
.nav-link {
  @apply text-steel-200 hover:text-white transition-colors duration-200 font-medium;
}

.dropdown-link {
  @apply block px-4 py-2 text-steel-700 hover:bg-steel-50 hover:text-accent-blue transition-colors duration-200;
}
</style>
