<template>
  <ToolPage module="color-filter" :params="params">
    <template #params>
      <div class="preset-row">
        <el-button
          v-for="p in presets"
          :key="p.value"
          :type="params.preset === p.value ? 'primary' : 'default'"
          size="small"
          round
          @click="params.preset = params.preset === p.value ? '' : p.value"
        >
          {{ p.label }}
        </el-button>
      </div>
      <ParamSlider v-model="params.brightness" label="亮度" :min="0" :max="2" :step="0.05" />
      <ParamSlider v-model="params.contrast" label="对比度" :min="0" :max="2" :step="0.05" />
      <ParamSlider v-model="params.saturation" label="饱和度" :min="0" :max="2" :step="0.05" />
      <ParamSlider v-model="params.temperature" label="色温" :min="-100" :max="100" :step="1" />
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  preset: '',
  brightness: 1.0,
  contrast: 1.0,
  saturation: 1.0,
  temperature: 0,
})

const presets = [
  { label: '暖色', value: 'warm' },
  { label: '冷色', value: 'cool' },
  { label: '黑白', value: 'bw' },
  { label: '复古', value: 'vintage' },
  { label: '日系', value: 'japanese' },
]
</script>

<style scoped>
.preset-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}
</style>
