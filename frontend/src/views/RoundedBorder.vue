<template>
  <ToolPage module="rounded-border" :params="params">
    <template #params>
      <ParamSlider v-model="params.radius" label="圆角半径" :min="0" :max="200" :step="1" unit="px" />
      <div class="param-row">
        <label class="param-label">边框宽度</label>
        <el-input-number v-model="params.border_size" :min="0" :max="100" />
      </div>
      <div class="param-row">
        <label class="param-label">边框颜色</label>
        <el-color-picker v-model="params.border_color" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  radius: 40,
  border_size: 0,
  border_color: '#ffffff',
})
</script>

<style scoped>
.param-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}
.param-label {
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
