<template>
  <ToolPage module="dehaze" :params="params">
    <template #params>
      <ParamSlider v-model="params.strength" label="去雾强度" :min="0" :max="2" :step="0.05" />
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'
import ParamSlider from '@/components/ParamSlider.vue'

const params = reactive<Record<string, unknown>>({
  strength: 1.0,
})
</script>
