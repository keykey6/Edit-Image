<template>
  <div class="tool-page">
    <div class="tool-upload">
      <div class="upload-area" @click="triggerInput">
        <el-icon class="upload-icon" :size="40"><UploadFilled /></el-icon>
        <p class="upload-text">点击选择多张图片</p>
        <p class="upload-hint">合并为单个 PDF 文件</p>
      </div>
      <input ref="fileInput" type="file" accept="image/*" multiple hidden @change="handleFiles" />
      <div v-if="files.length" class="file-list">
        <el-tag v-for="(f, i) in files" :key="i" closable @close="files.splice(i, 1)">{{ f.name }}</el-tag>
      </div>
    </div>

    <div v-if="files.length" class="tool-actions">
      <el-button type="primary" size="large" round :loading="processing" @click="handleProcess">
        {{ processing ? '转换中...' : `转为 PDF（${files.length} 张）` }}
      </el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="resultUrl" class="tool-result">
      <el-result icon="success" title="PDF 已生成">
        <template #extra>
          <el-button type="success" size="large" round @click="handleDownload">下载 PDF</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'

const files = ref<File[]>([])
const fileInput = ref<HTMLInputElement>()
const processing = ref(false)
const errorMsg = ref('')
const resultUrl = ref<string>()
const resultBlob = ref<Blob>()

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
    const res = await api.post('/to-pdf/process', fd, { responseType: 'blob' })
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '转换失败'
  } finally { processing.value = false }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a'); a.href = url; a.download = 'output.pdf'; a.click()
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
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.tool-result { margin-top: 8px; }
</style>
