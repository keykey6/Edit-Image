<template>
  <ToolPage module="remove-bg" :params="params">
    <template #params>
      <div class="param-row">
        <label>Alpha 精细化（处理更慢但边缘更好）</label>
        <el-switch v-model="params.alpha_matting" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive<Record<string, unknown>>({
  alpha_matting: false,
})
</script>

<style scoped>
.param-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
}
.param-row label {
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
