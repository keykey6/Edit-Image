<template>
  <ToolPage module="compress" :params="params">
    <template #params>
      <ParamSlider v-model="params.quality" label="压缩质量" :min="1" :max="100" />
      <div class="param-group">
        <label class="param-label">最大尺寸（像素，0=不限）</label>
        <el-input-number v-model="params.max_size" :min="0" :max="10000" :step="100" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  quality: 70,
  max_size: 0,
})
</script>

<style scoped>
.param-group {
  margin-top: 16px;
}
.param-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}
</style>
