<template>
  <ToolPage module="watermark-remove" :params="params">
    <template #params>
      <div class="param-group">
        <label class="param-label">去除方法</label>
        <el-radio-group v-model="params.method">
          <el-radio-button value="crop">裁剪边缘</el-radio-button>
          <el-radio-button value="blur">边缘模糊</el-radio-button>
          <el-radio-button value="inpaint">智能修复</el-radio-button>
        </el-radio-group>
      </div>
      <ParamSlider v-model="params.margin" label="处理边距" :min="5" :max="100" :step="1" unit="px" />
      <p class="hint">裁剪/模糊/修复图片边缘区域（常用于去除水印、logo等）</p>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  method: 'crop',
  margin: 20,
})
</script>

<style scoped>
.param-group {
  margin-top: 4px;
  margin-bottom: 16px;
}
.param-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}
.hint {
  margin-top: 12px;
  font-size: 12px;
  color: var(--text-secondary);
}
</style>
