<template>
  <ToolPage module="grid-split" :params="params">
    <template #params>
      <div class="param-row">
        <div class="param-item">
          <label class="param-label">行数</label>
          <el-input-number v-model="params.rows" :min="1" :max="10" />
        </div>
        <div class="param-item">
          <label class="param-label">列数</label>
          <el-input-number v-model="params.cols" :min="1" :max="10" />
        </div>
      </div>
      <p class="hint">图片将被切成 {{ params.rows }} × {{ params.cols }} 块，打包为 zip 下载</p>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive<Record<string, unknown>>({
  rows: 2,
  cols: 2,
})
</script>

<style scoped>
.param-row {
  display: flex;
  gap: 24px;
}
.param-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.param-label {
  font-size: 13px;
  color: var(--text-secondary);
}
.hint {
  margin-top: 16px;
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
