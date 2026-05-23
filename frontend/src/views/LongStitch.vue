<template>
  <div class="tool-page">
    <div class="tool-upload">
      <div class="upload-area" @click="triggerInput">
        <el-icon class="upload-icon" :size="40"><UploadFilled /></el-icon>
        <p class="upload-text">点击选择多张图片（至少2张）</p>
        <p class="upload-hint">按选择顺序纵向或横向拼接</p>
      </div>
      <input ref="fileInput" type="file" accept="image/*" multiple hidden @change="handleFiles" />
      <div v-if="files.length" class="file-list">
        <el-tag v-for="(f, i) in files" :key="i" closable @close="files.splice(i, 1)">{{ f.name }}</el-tag>
      </div>
    </div>

    <div class="tool-params">
      <div class="param-row">
        <span class="param-label">方向</span>
        <el-radio-group v-model="params.direction" size="small">
          <el-radio-button value="vertical">纵向</el-radio-button>
          <el-radio-button value="horizontal">横向</el-radio-button>
        </el-radio-group>
      </div>
      <div class="param-row">
        <span class="param-label">间距 (px)</span>
        <el-input-number v-model="params.gap" :min="0" :max="100" size="small" />
      </div>
    </div>

    <div v-if="files.length >= 2" class="tool-actions">
      <el-button type="primary" size="large" round :loading="processing" @click="handleProcess">
        {{ processing ? '拼接中...' : '开始拼接' }}
      </el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="resultUrl" class="tool-result">
      <img :src="resultUrl" class="result-img" />
      <div class="tool-download">
        <el-button type="success" size="large" round @click="handleDownload">下载长图</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import api from '@/api'

const files = ref<File[]>([])
const fileInput = ref<HTMLInputElement>()
const processing = ref(false)
const errorMsg = ref('')
const resultUrl = ref<string>()
const resultBlob = ref<Blob>()
const params = reactive({ direction: 'vertical', gap: 0 })

function triggerInput() { fileInput.value?.click() }
function handleFiles(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files) files.value = [...files.value, ...Array.from(input.files)]
}

async function handleProcess() {
  processing.value = true; errorMsg.value = ''
  try {
    const fd = new FormData()
    for (const f of files.value) fd.append('files', f)
    fd.append('params', JSON.stringify(params))
    const res = await api.post('/long-stitch/process', fd, { responseType: 'blob' })
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '拼接失败'
  } finally { processing.value = false }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a'); a.href = url; a.download = 'stitch.png'; a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.tool-page { max-width: 900px; margin: 0 auto; }
.tool-upload { margin-bottom: 24px; }
.upload-area { border: 2px dashed var(--border-color); border-radius: var(--radius); padding: 36px 24px; text-align: center; cursor: pointer; transition: border-color 0.3s; }
.upload-area:hover { border-color: var(--primary); background: rgba(108, 92, 231, 0.04); }
.upload-icon { color: var(--primary-light); margin-bottom: 12px; }
.upload-text { font-size: 15px; color: var(--text-primary); margin-bottom: 6px; }
.upload-hint { font-size: 12px; color: var(--text-secondary); }
.file-list { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
.tool-params { background: var(--card-bg); border-radius: var(--radius); padding: 20px 24px; margin-bottom: 24px; box-shadow: var(--shadow); }
.param-row { display: flex; align-items: center; gap: 16px; margin-bottom: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.tool-result { text-align: center; }
.result-img { max-width: 100%; max-height: 500px; border-radius: 12px; box-shadow: var(--shadow); }
.tool-download { margin-top: 24px; }
</style>
