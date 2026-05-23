<template>
  <ToolPage module="dpi" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">DPI 值</span>
        <el-input-number v-model="params.dpi" :min="1" :max="1200" :step="1" size="small" />
        <span class="param-hint">（常用：72 / 150 / 300）</span>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ dpi: 300 })
</script>

<style scoped>
.param-row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.param-label { font-weight: 600; font-size: 14px; min-width: 60px; }
.param-hint { font-size: 12px; color: var(--text-secondary); }
</style>
