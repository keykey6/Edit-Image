<template>
  <ToolPage module="perspective" :params="params">
    <template #params>
      <div class="param-hint">
        输入4组坐标 (左上, 右上, 右下, 左下)，值范围 0.0 ~ 1.0（相对图片尺寸的比例）
      </div>
      <div class="pts-grid">
        <div v-for="(pt, i) in labels" :key="i" class="pt-input">
          <span class="pt-label">{{ pt }}</span>
          <el-input-number v-model="params.points[i][0]" :min="0" :max="1" :step="0.01" :precision="2" size="small" controls-position="right" />
          <el-input-number v-model="params.points[i][1]" :min="0" :max="1" :step="0.01" :precision="2" size="small" controls-position="right" />
        </div>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const labels = ['左上', '右上', '右下', '左下']
const params = reactive({
  points: [
    [0.1, 0.1],
    [0.9, 0.1],
    [0.9, 0.9],
    [0.1, 0.9],
  ] as [number, number][],
})
</script>

<style scoped>
.param-hint { font-size: 13px; color: var(--text-secondary); margin-bottom: 16px; }
.pts-grid { display: flex; flex-wrap: wrap; gap: 12px; }
.pt-input { display: flex; align-items: center; gap: 8px; }
.pt-label { font-weight: 600; font-size: 13px; width: 36px; }
</style>
