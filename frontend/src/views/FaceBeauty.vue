<template>
  <ToolPage module="face-beauty" :params="params">
    <template #params>
      <ParamSlider v-model="params.smooth" label="磨皮强度" :min="0" :max="1" :step="0.05" />
      <ParamSlider v-model="params.whiten" label="美白强度" :min="0" :max="1" :step="0.05" />
      <ParamSlider v-model="params.sharpen" label="锐化强度" :min="0" :max="1" :step="0.05" />
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  smooth: 0.5,
  whiten: 0.3,
  sharpen: 0.3,
})
</script>
