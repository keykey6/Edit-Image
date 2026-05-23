<template>
  <ToolPage module="text-to-image" :params="params">
    <template #params>
      <div class="param-row">
        <span class="param-label">文字内容</span>
        <el-input v-model="params.text" type="textarea" :rows="4" placeholder="输入要渲染的文字" size="small" style="width: 320px" />
      </div>
      <div class="param-row">
        <span class="param-label">字体大小</span>
        <el-input-number v-model="params.font_size" :min="8" :max="200" :step="1" size="small" />
      </div>
      <div class="param-row">
        <span class="param-label">文字颜色</span>
        <el-color-picker v-model="params.text_color" size="small" />
        <span class="param-label">背景色</span>
        <el-color-picker v-model="params.bg_color" size="small" />
      </div>
      <div class="param-row">
        <span class="param-label">对齐</span>
        <el-radio-group v-model="params.align" size="small">
          <el-radio-button value="left">左对齐</el-radio-button>
          <el-radio-button value="center">居中</el-radio-button>
          <el-radio-button value="right">右对齐</el-radio-button>
        </el-radio-group>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive({ text: '', font_size: 32, text_color: '#333333', bg_color: '#FFFFFF', align: 'center' })
</script>

<style scoped>
.param-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
</style>
