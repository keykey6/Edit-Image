<template>
  <ToolPage module="crop-rotate" :params="params">
    <template #params>
      <div class="param-group">
        <label class="param-label">操作</label>
        <el-select v-model="params.action" style="width: 200px">
          <el-option label="水平翻转" value="flip_h" />
          <el-option label="垂直翻转" value="flip_v" />
          <el-option label="旋转" value="rotate" />
        </el-select>
      </div>
      <div v-if="params.action === 'rotate'" class="param-group">
        <label class="param-label">旋转角度</label>
        <el-slider v-model="params.angle" :min="-180" :max="180" :step="1" show-input />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive<Record<string, unknown>>({
  action: 'flip_h',
  angle: 0,
})
</script>

<style scoped>
.param-group {
  margin-top: 16px;
}
.param-group:first-child {
  margin-top: 4px;
}
.param-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}
</style>
