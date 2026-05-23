<template>
  <ToolPage module="format-convert" :params="params">
    <template #params>
      <div class="param-group">
        <label class="param-label">目标格式</label>
        <el-select v-model="params.format" style="width: 200px">
          <el-option label="PNG" value="png" />
          <el-option label="JPEG" value="jpeg" />
          <el-option label="WebP" value="webp" />
          <el-option label="BMP" value="bmp" />
        </el-select>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive<Record<string, unknown>>({
  format: 'png',
})
</script>

<style scoped>
.param-group {
  margin-top: 4px;
}
.param-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}
</style>
