<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div v-if="file" class="tool-actions">
      <el-button type="primary" size="large" round :loading="loading" @click="analyze">分析配色</el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="result" class="result-panel">
      <h3 class="result-title">主色调分析</h3>
      <div class="palette">
        <div v-for="(c, i) in result.colors" :key="i" class="color-card">
          <div class="color-swatch" :style="{ background: c.hex }" />
          <div class="color-info">
            <span class="color-hex">{{ c.hex }}</span>
            <span class="color-rgb">RGB({{ c.r }}, {{ c.g }}, {{ c.b }})</span>
            <span class="color-ratio">{{ c.ratio }}%</span>
          </div>
          <div class="color-bar">
            <div class="color-bar-fill" :style="{ width: c.ratio + '%', background: c.hex }" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'
import ImageUploader from '@/components/ImageUploader.vue'

interface ColorItem { hex: string; r: number; g: number; b: number; ratio: number }

const file = ref<File | null>(null)
const loading = ref(false)
const errorMsg = ref('')
const result = ref<{ colors: ColorItem[] }>()

async function analyze() {
  if (!file.value) return
  loading.value = true; errorMsg.value = ''
  try {
    const fd = new FormData()
    fd.append('file', file.value)
    fd.append('params', JSON.stringify({ clusters: 6 }))
    const res = await api.post('/color-analysis/process', fd)
    result.value = res.data
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '分析失败'
  } finally { loading.value = false }
}
</script>

<style scoped>
.tool-page { max-width: 700px; margin: 0 auto; }
.tool-upload { margin-bottom: 24px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.result-panel { background: var(--card-bg); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); }
.result-title { margin: 0 0 20px 0; font-size: 18px; }
.palette { display: flex; flex-direction: column; gap: 14px; }
.color-card { display: flex; align-items: center; gap: 14px; }
.color-swatch { width: 48px; height: 48px; border-radius: 10px; flex-shrink: 0; box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
.color-info { display: flex; flex-direction: column; gap: 2px; min-width: 140px; }
.color-hex { font-weight: 700; font-size: 16px; }
.color-rgb { font-size: 12px; color: var(--text-secondary); }
.color-ratio { font-size: 12px; color: var(--primary); }
.color-bar { flex: 1; height: 8px; background: #eee; border-radius: 4px; overflow: hidden; }
.color-bar-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
</style>
