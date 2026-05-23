<template>
  <ToolPage module="barcode" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">内容</span>
        <el-input v-model="params.text" placeholder="输入条形码内容" size="small" style="width: 240px" />
      </div>
      <div class="param-row">
        <span class="param-label">格式</span>
        <el-select v-model="params.format" size="small" style="width: 160px">
          <el-option label="Code128" value="code128" />
          <el-option label="EAN-13" value="ean13" />
          <el-option label="EAN-8" value="ean8" />
          <el-option label="UPC-A" value="upca" />
          <el-option label="Code39" value="code39" />
          <el-option label="ISBN-13" value="isbn13" />
        </el-select>
      </div>
      <div class="param-row">
        <span class="param-label">宽度</span>
        <el-input-number v-model="params.width" :min="0.1" :max="1" :step="0.05" :precision="2" size="small" />
        <span class="param-label">高度</span>
        <el-input-number v-model="params.height" :min="5" :max="50" :step="1" size="small" />
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ text: '123456789012', format: 'code128', width: 0.3, height: 20 })
</script>

<style scoped>
.param-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
</style>
