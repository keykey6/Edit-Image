<template>
  <ToolPage module="meme" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">顶部文字</span>
        <el-input v-model="params.top_text" placeholder="（可选）" size="small" style="width: 280px" />
      </div>
      <div class="param-row">
        <span class="param-label">底部文字</span>
        <el-input v-model="params.bottom_text" placeholder="（可选）" size="small" style="width: 280px" />
      </div>
      <div class="param-row">
        <span class="param-label">字体大小</span>
        <el-input-number v-model="params.font_size" :min="12" :max="120" :step="2" size="small" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ top_text: '', bottom_text: '', font_size: 40 })
</script>

<style scoped>
.param-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.param-label { font-weight: 600; font-size: 14px; min-width: 70px; }
</style>
