<template>
  <ToolPage module="shadow" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">倒影高度 (%)</span>
        <el-slider v-model="params.height" :min="10" :max="100" :step="5" show-input style="width: 200px" />
      </div>
      <div class="param-row">
        <span class="param-label">透明度</span>
        <el-slider v-model="params.opacity" :min="0.1" :max="1" :step="0.1" show-input style="width: 200px" />
      </div>
      <div class="param-row">
        <span class="param-label">模糊程度</span>
        <el-slider v-model="params.blur" :min="0" :max="20" :step="1" show-input style="width: 200px" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ height: 30, opacity: 0.5, blur: 5 })
</script>

<style scoped>
.param-row { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
.param-label { font-weight: 600; font-size: 14px; min-width: 100px; }
</style>
