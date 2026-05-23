<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div class="tool-params">
      <div class="param-row">
        <span class="param-label">X 坐标</span>
        <el-input-number v-model="x" :min="0" :max="9999" size="small" />
        <span class="param-label">Y 坐标</span>
        <el-input-number v-model="y" :min="0" :max="9999" size="small" />
      </div>
      <div class="param-row">
        <span class="param-label">采样半径</span>
        <el-input-number v-model="radius" :min="0" :max="50" size="small" />
        <span class="param-hint">（0 表示单像素，>0 取周边平均）</span>
      </div>
    </div>

    <div v-if="file" class="tool-actions">
      <el-button type="primary" size="large" round :loading="loading" @click="pickColor">取色</el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="result" class="result-panel">
      <div class="color-preview" :style="{ background: result.hex }">
        <span class="color-text">{{ result.hex }}</span>
      </div>
      <div class="color-meta">
        <div class="meta-item">
          <span class="meta-label">HEX</span>
          <span class="meta-value">{{ result.hex }}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">RGB</span>
          <span class="meta-value">rgb({{ result.r }}, {{ result.g }}, {{ result.b }})</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'
import ImageUploader from '@/components/ImageUploader.vue'

const file = ref<File | null>(null)
const x = ref(0)
const y = ref(0)
const radius = ref(0)
const loading = ref(false)
const errorMsg = ref('')
const result = ref<any>()

async function pickColor() {
  if (!file.value) return
  loading.value = true; errorMsg.value = ''
  try {
    const fd = new FormData()
    fd.append('file', file.value)
    fd.append('params', JSON.stringify({ x: x.value, y: y.value, radius: radius.value }))
    const res = await api.post('/color-picker/process', fd)
    result.value = res.data
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '取色失败'
  } finally { loading.value = false }
}
</script>

<style scoped>
.tool-page { max-width: 700px; margin: 0 auto; }
.tool-upload { margin-bottom: 24px; }
.tool-params { background: var(--card-bg); border-radius: var(--radius); padding: 20px 24px; margin-bottom: 24px; box-shadow: var(--shadow); }
.param-row { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
.param-hint { font-size: 12px; color: var(--text-secondary); }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.result-panel { background: var(--card-bg); border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow); }
.color-preview { height: 140px; display: flex; align-items: center; justify-content: center; }
.color-text { font-size: 32px; font-weight: 800; mix-blend-mode: difference; color: #fff; }
.color-meta { padding: 20px 24px; display: flex; gap: 32px; }
.meta-item { display: flex; flex-direction: column; gap: 4px; }
.meta-label { font-size: 12px; color: var(--text-secondary); }
.meta-value { font-size: 16px; font-weight: 600; font-family: monospace; }
</style>
