<template>
  <ToolPage module="photo-restore" :params="params">
    <template #params>
      <ParamSlider v-model="params.denoise" label="去噪强度" :min="0" :max="1" :step="0.05" />
      <div class="param-row">
        <label>修复划痕</label>
        <el-switch v-model="params.fix_scratches" />
      </div>
      <div class="param-row">
        <label>色彩校正</label>
        <el-switch v-model="params.correct_color" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  denoise: 0.5,
  fix_scratches: true,
  correct_color: true,
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
.param-row label {
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
