<template>
  <ToolPage module="histogram">
    <template #params>
      <p class="desc">上传图片，自动生成 RGB 三通道像素分布直方图</p>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import ToolPage from '@/components/ToolPage.vue'
</script>

<style scoped>
.desc { font-size: 14px; color: var(--text-secondary); margin: 0; }
</style>
