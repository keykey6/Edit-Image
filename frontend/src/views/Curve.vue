<template>
  <ToolPage module="curve" :params="params">
    <template #params>
      <div class="param-group">
        <span class="param-label">通道</span>
        <el-radio-group v-model="params.channel" size="small">
          <el-radio-button value="rgb">RGB 全通道</el-radio-button>
          <el-radio-button value="r">红</el-radio-button>
          <el-radio-button value="g">绿</el-radio-button>
          <el-radio-button value="b">蓝</el-radio-button>
        </el-radio-group>
      </div>
      <div class="param-group">
        <span class="param-label">曲线点（0-100）</span>
        <span class="param-hint">格式：输入,输出 用空格分隔多组，如 "0,0 50,60 100,100"</span>
        <el-input v-model="pointsText" placeholder="0,0 100,100" size="small" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const channel = ref('rgb')
const pointsText = ref('0,0 50,50 100,100')

const params = computed(() => {
  const pts = pointsText.value.trim().split(/\s+/).map(s => {
    const [x, y] = s.split(',').map(Number)
    return [x, y]
  })
  return { channel: channel.value, points: pts }
})
</script>

<style scoped>
.param-group { margin-bottom: 16px; }
.param-label { display: block; font-weight: 600; font-size: 14px; margin-bottom: 8px; }
.param-hint { display: block; font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; }
</style>
