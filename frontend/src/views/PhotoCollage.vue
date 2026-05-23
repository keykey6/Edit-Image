<template>
  <div class="tool-page">
    <div class="tool-upload">
      <div class="upload-area" @click="triggerInput">
        <el-icon class="upload-icon" :size="40"><UploadFilled /></el-icon>
        <p class="upload-text">点击选择多张图片（至少2张）</p>
        <p class="upload-hint">按选择顺序排列</p>
      </div>
      <input ref="fileInput" type="file" accept="image/*" multiple hidden @change="handleFiles" />
      <div v-if="files.length" class="file-list">
        <el-tag v-for="(f, i) in files" :key="i" closable @close="files.splice(i, 1)">
          {{ f.name }}
        </el-tag>
      </div>
      <p v-if="files.length" class="file-count">已选择 {{ files.length }} 张图片</p>
    </div>

    <div class="tool-params">
      <div class="param-row">
        <div class="param-item">
          <label class="param-label">行数</label>
          <el-input-number v-model="params.rows" :min="1" :max="6" />
        </div>
        <div class="param-item">
          <label class="param-label">列数</label>
          <el-input-number v-model="params.cols" :min="1" :max="6" />
        </div>
        <div class="param-item">
          <label class="param-label">间距 (px)</label>
          <el-input-number v-model="params.spacing" :min="0" :max="50" />
        </div>
      </div>
    </div>

    <div v-if="files.length >= 2" class="tool-actions">
      <el-button type="primary" size="large" round :loading="processing" @click="handleProcess">
        <el-icon v-if="!processing"><Grid /></el-icon>
        {{ processing ? '拼图中...' : '开始拼图' }}
      </el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="resultUrl" class="tool-result">
      <img :src="resultUrl" class="result-img" />
      <div class="tool-download">
        <el-button type="success" size="large" round @click="handleDownload">
          <el-icon><Download /></el-icon>
          下载拼图
        </el-button>
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

const params = reactive<Record<string, unknown>>({
  rows: 2,
  cols: 2,
  spacing: 8,
})

function triggerInput() {
  fileInput.value?.click()
}

function handleFiles(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files) {
    files.value = [...files.value, ...Array.from(input.files)]
  }
}

async function handleProcess() {
  if (files.value.length < 2) return
  processing.value = true
  errorMsg.value = ''
  try {
    const formData = new FormData()
    for (const f of files.value) {
      formData.append('files', f)
    }
    formData.append('params', JSON.stringify(params))
    const res = await api.post('/photo-collage/process', formData, { responseType: 'blob' })
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '拼图失败'
  } finally {
    processing.value = false
  }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a')
  a.href = url
  a.download = 'collage.png'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.tool-page { max-width: 900px; margin: 0 auto; }
.tool-upload { margin-bottom: 16px; }
.file-count { margin-top: 8px; font-size: 13px; color: var(--primary); }
.tool-params {
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow);
}
.param-row { display: flex; gap: 24px; }
.param-item { display: flex; flex-direction: column; gap: 6px; }
.param-label { font-size: 13px; color: var(--text-secondary); }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.tool-result { text-align: center; }
.result-img { max-width: 100%; max-height: 500px; border-radius: 12px; box-shadow: var(--shadow); }
.tool-download { margin-top: 24px; }
</style>
