<template>
  <div class="min-h-screen bg-gradient-to-br from-steel-50 to-industrial-100">
    <!-- 头部区域 -->
    <section class="bg-gradient-to-r from-steel-800 to-steel-900 text-white py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-6">
            产品演示
          </h1>
          <p class="text-xl text-steel-200 mb-8 max-w-3xl mx-auto">
            体验SemiX半导体出海信息服务平台的核心功能
          </p>
        </div>
      </div>
    </section>

    <!-- 演示内容区域 -->
    <section class="py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 功能演示选项卡 -->
        <div class="mb-12">
          <div class="flex flex-wrap justify-center gap-4 mb-8">
            <button
              v-for="demo in demos"
              :key="demo.id"
              @click="activeDemo = demo.id"
              :class="[
                'px-6 py-3 rounded-industrial font-medium transition-all duration-200',
                activeDemo === demo.id
                  ? 'bg-accent-blue text-white shadow-lg'
                  : 'bg-white text-steel-700 hover:bg-steel-50 border border-steel-200'
              ]"
            >
              {{ demo.title }}
            </button>
          </div>
        </div>

        <!-- 演示内容 -->
        <div class="bg-white rounded-industrial shadow-industrial-lg overflow-hidden">
          <div v-if="activeDemo === 'policy'" class="p-8">
            <h3 class="text-2xl font-bold text-steel-800 mb-6">政策监控台演示</h3>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h4 class="text-lg font-semibold text-steel-700 mb-4">实时政策更新</h4>
                <div class="space-y-4">
                  <div v-for="policy in mockPolicies" :key="policy.id" 
                       class="border border-steel-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between mb-2">
                      <span :class="['px-2 py-1 rounded text-xs font-medium', policy.urgency === 'high' ? 'bg-red-100 text-red-800' : policy.urgency === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800']">
                        {{ policy.country }}
                      </span>
                      <span class="text-sm text-steel-500">{{ policy.date }}</span>
                    </div>
                    <h5 class="font-medium text-steel-800 mb-2">{{ policy.title }}</h5>
                    <p class="text-sm text-steel-600">{{ policy.summary }}</p>
                  </div>
                </div>
              </div>
              <div>
                <h4 class="text-lg font-semibold text-steel-700 mb-4">政策影响分析</h4>
                <div class="bg-steel-50 rounded-lg p-6">
                  <div class="text-center mb-4">
                    <div class="text-3xl font-bold text-accent-blue">85%</div>
                    <div class="text-sm text-steel-600">政策合规度</div>
                  </div>
                  <div class="space-y-3">
                    <div class="flex justify-between items-center">
                      <span class="text-sm text-steel-600">日本市场</span>
                      <div class="w-24 bg-steel-200 rounded-full h-2">
                        <div class="bg-green-500 h-2 rounded-full" style="width: 90%"></div>
                      </div>
                    </div>
                    <div class="flex justify-between items-center">
                      <span class="text-sm text-steel-600">韩国市场</span>
                      <div class="w-24 bg-steel-200 rounded-full h-2">
                        <div class="bg-yellow-500 h-2 rounded-full" style="width: 75%"></div>
                      </div>
                    </div>
                    <div class="flex justify-between items-center">
                      <span class="text-sm text-steel-600">新加坡市场</span>
                      <div class="w-24 bg-steel-200 rounded-full h-2">
                        <div class="bg-green-500 h-2 rounded-full" style="width: 95%"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeDemo === 'supplier'" class="p-8">
            <h3 class="text-2xl font-bold text-steel-800 mb-6">供应商目录演示</h3>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div v-for="supplier in mockSuppliers" :key="supplier.id"
                   class="border border-steel-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div class="flex items-center justify-between mb-4">
                  <h4 class="font-semibold text-steel-800">{{ supplier.name }}</h4>
                  <span :class="['px-2 py-1 rounded text-xs font-medium', supplier.verified ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800']">
                    {{ supplier.verified ? '已认证' : '待认证' }}
                  </span>
                </div>
                <div class="space-y-2 text-sm text-steel-600">
                  <div class="flex items-center">
                    <span class="w-16">地区:</span>
                    <span>{{ supplier.region }}</span>
                  </div>
                  <div class="flex items-center">
                    <span class="w-16">产品:</span>
                    <span>{{ supplier.products }}</span>
                  </div>
                  <div class="flex items-center">
                    <span class="w-16">评级:</span>
                    <div class="flex">
                      <span v-for="i in 5" :key="i" 
                            :class="i <= supplier.rating ? 'text-yellow-400' : 'text-steel-300'">★</span>
                    </div>
                  </div>
                </div>
                <button class="mt-4 w-full bg-accent-blue text-white py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  查看详情
                </button>
              </div>
            </div>
          </div>

          <div v-if="activeDemo === 'market'" class="p-8">
            <h3 class="text-2xl font-bold text-steel-800 mb-6">市场情报演示</h3>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h4 class="text-lg font-semibold text-steel-700 mb-4">价格趋势</h4>
                <div class="bg-steel-50 rounded-lg p-6">
                  <div class="flex justify-between items-center mb-4">
                    <span class="text-sm font-medium text-steel-700">存储芯片价格指数</span>
                    <span class="text-lg font-bold text-green-600">+12.5%</span>
                  </div>
                  <div class="h-32 bg-gradient-to-r from-green-400 to-blue-500 rounded-lg flex items-end justify-center">
                    <span class="text-white font-medium mb-4">📈 价格上涨趋势</span>
                  </div>
                </div>
              </div>
              <div>
                <h4 class="text-lg font-semibold text-steel-700 mb-4">需求预测</h4>
                <div class="space-y-4">
                  <div class="bg-steel-50 rounded-lg p-4">
                    <div class="flex justify-between items-center mb-2">
                      <span class="font-medium text-steel-700">汽车芯片</span>
                      <span class="text-green-600 font-medium">↗ +25%</span>
                    </div>
                    <div class="w-full bg-steel-200 rounded-full h-2">
                      <div class="bg-green-500 h-2 rounded-full" style="width: 75%"></div>
                    </div>
                  </div>
                  <div class="bg-steel-50 rounded-lg p-4">
                    <div class="flex justify-between items-center mb-2">
                      <span class="font-medium text-steel-700">工业芯片</span>
                      <span class="text-blue-600 font-medium">↗ +18%</span>
                    </div>
                    <div class="w-full bg-steel-200 rounded-full h-2">
                      <div class="bg-blue-500 h-2 rounded-full" style="width: 60%"></div>
                    </div>
                  </div>
                  <div class="bg-steel-50 rounded-lg p-4">
                    <div class="flex justify-between items-center mb-2">
                      <span class="font-medium text-steel-700">消费电子</span>
                      <span class="text-yellow-600 font-medium">→ +5%</span>
                    </div>
                    <div class="w-full bg-steel-200 rounded-full h-2">
                      <div class="bg-yellow-500 h-2 rounded-full" style="width: 45%"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="activeDemo === 'compliance'" class="p-8">
            <h3 class="text-2xl font-bold text-steel-800 mb-6">合规工具演示</h3>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h4 class="text-lg font-semibold text-steel-700 mb-4">HS编码查询</h4>
                <div class="space-y-4">
                  <div class="flex gap-4">
                    <input 
                      type="text" 
                      placeholder="输入产品名称或编码"
                      class="flex-1 px-4 py-2 border border-steel-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-blue"
                      v-model="hsCodeQuery"
                    />
                    <button class="px-6 py-2 bg-accent-blue text-white rounded-lg hover:bg-blue-700">
                      查询
                    </button>
                  </div>
                  <div v-if="hsCodeQuery" class="bg-steel-50 rounded-lg p-4">
                    <div class="font-medium text-steel-800 mb-2">查询结果:</div>
                    <div class="text-sm text-steel-600">
                      <div>HS编码: 8542.31.0000</div>
                      <div>产品描述: 处理器和控制器</div>
                      <div>税率: 0% (中日EPA)</div>
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <h4 class="text-lg font-semibold text-steel-700 mb-4">出口许可检查</h4>
                <div class="space-y-4">
                  <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div class="flex items-center mb-2">
                      <span class="text-green-600 mr-2">✓</span>
                      <span class="font-medium text-green-800">日本出口许可</span>
                    </div>
                    <div class="text-sm text-green-700">无需特殊许可，可正常出口</div>
                  </div>
                  <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div class="flex items-center mb-2">
                      <span class="text-yellow-600 mr-2">⚠</span>
                      <span class="font-medium text-yellow-800">韩国出口许可</span>
                    </div>
                    <div class="text-sm text-yellow-700">需要申请特殊许可证</div>
                  </div>
                  <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div class="flex items-center mb-2">
                      <span class="text-green-600 mr-2">✓</span>
                      <span class="font-medium text-green-800">新加坡出口许可</span>
                    </div>
                    <div class="text-sm text-green-700">符合ASEAN贸易协定</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 行动号召 -->
        <div class="text-center mt-12">
          <h3 class="text-2xl font-bold text-steel-800 mb-4">准备开始使用了吗？</h3>
          <p class="text-steel-600 mb-8">立即注册，获取完整功能访问权限</p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <RouterLink to="/register" class="btn-primary text-lg px-8 py-3">
              免费注册
            </RouterLink>
            <RouterLink to="/login" class="btn-secondary text-lg px-8 py-3">
              已有账户？登录
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const activeDemo = ref('policy')
const hsCodeQuery = ref('')

const demos = [
  { id: 'policy', title: '政策监控' },
  { id: 'supplier', title: '供应商目录' },
  { id: 'market', title: '市场情报' },
  { id: 'compliance', title: '合规工具' }
]

const mockPolicies = [
  {
    id: 1,
    country: '日本',
    title: '半导体制造设备出口管制新规',
    summary: '针对先进制程设备的出口限制措施',
    date: '2024-01-15',
    urgency: 'high'
  },
  {
    id: 2,
    country: '韩国',
    title: 'K-半导体带政策更新',
    summary: '政府投资激励政策调整',
    date: '2024-01-12',
    urgency: 'medium'
  },
  {
    id: 3,
    country: '新加坡',
    title: '东南亚制造中心优惠政策',
    summary: '税收减免和投资补贴政策',
    date: '2024-01-10',
    urgency: 'low'
  }
]

const mockSuppliers = [
  {
    id: 1,
    name: 'Tokyo Semiconductor',
    region: '日本东京',
    products: '存储芯片',
    rating: 5,
    verified: true
  },
  {
    id: 2,
    name: 'Seoul Tech Solutions',
    region: '韩国首尔',
    products: '处理器',
    rating: 4,
    verified: true
  },
  {
    id: 3,
    name: 'Singapore Micro',
    region: '新加坡',
    products: '传感器',
    rating: 4,
    verified: false
  }
]
</script>
