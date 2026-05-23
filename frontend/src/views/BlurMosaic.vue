<template>
  <ToolPage module="blur-mosaic" :params="params">
    <template #params>
      <div class="param-group">
        <label class="param-label">效果类型</label>
        <el-radio-group v-model="params.type">
          <el-radio-button value="gaussian">高斯模糊</el-radio-button>
          <el-radio-button value="mosaic">像素化马赛克</el-radio-button>
        </el-radio-group>
      </div>
      <ParamSlider
        v-if="params.type === 'gaussian'"
        v-model="params.kernel_size"
        label="模糊强度"
        :min="3" :max="51" :step="2"
      />
      <ParamSlider
        v-else
        v-model="params.block_size"
        label="马赛克块大小"
        :min="2" :max="40" :step="1"
      />
      <div class="param-row">
        <label>人脸自动检测打码</label>
        <el-switch v-model="params.face_detect" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  type: 'gaussian',
  kernel_size: 15,
  block_size: 10,
  face_detect: false,
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
.param-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid var(--border-color);
  margin-top: 16px;
}
.param-row label {
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
