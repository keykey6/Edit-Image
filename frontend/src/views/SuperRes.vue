<template>
  <ToolPage module="super-res" :params="params">
    <template #params>
      <ParamSlider v-model="params.scale" label="放大倍数" :min="1" :max="4" :step="0.1" unit="x" />
      <ParamSlider v-model="params.sharpen" label="锐化强度" :min="0" :max="1" :step="0.05" />
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  scale: 2.0,
  sharpen: 0.5,
})
</script>
