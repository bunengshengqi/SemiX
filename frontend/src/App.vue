<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="min-h-screen bg-industrial-50">
    <!-- 导航栏 -->
    <Navbar />

    <!-- 主要内容区域 -->
    <main>
      <RouterView />
    </main>
  </div>
</template>


