<template>
  <ToolPage module="hsl" :params="params">
    <template #params>
      <div class="param-slider">
        <span class="param-label">色相偏移 <em>{{ params.hue }}</em></span>
        <el-slider v-model="params.hue" :min="-180" :max="180" :step="1" show-input />
      </div>
      <div class="param-slider">
        <span class="param-label">饱和度 <em>{{ params.saturation }}</em></span>
        <el-slider v-model="params.saturation" :min="-100" :max="100" :step="1" show-input />
      </div>
      <div class="param-slider">
        <span class="param-label">明度 <em>{{ params.lightness }}</em></span>
        <el-slider v-model="params.lightness" :min="-100" :max="100" :step="1" show-input />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ hue: 0, saturation: 0, lightness: 0 })
</script>

<style scoped>
.param-slider { margin-bottom: 20px; }
.param-label { display: block; font-weight: 600; font-size: 14px; margin-bottom: 8px; }
.param-label em { font-style: normal; color: var(--primary); margin-left: 4px; }
</style>
