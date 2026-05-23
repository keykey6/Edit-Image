<template>
  <ToolPage module="privacy-erase" :params="params">
    <template #params>
      <div class="param-row">
        <el-checkbox v-model="params.remove_exif">移除 EXIF 元数据（拍摄设备、GPS位置等）</el-checkbox>
      </div>
      <div class="param-row">
        <el-checkbox v-model="params.remove_icc">移除 ICC 色彩配置</el-checkbox>
      </div>
      <div class="param-row">
        <el-checkbox v-model="params.remove_thumbnail">移除内嵌缩略图</el-checkbox>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ remove_exif: true, remove_icc: true, remove_thumbnail: true })
</script>

<style scoped>
.param-row { margin-bottom: 12px; }
</style>
