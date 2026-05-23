<template>
  <div class="tool-page">
    <div class="tool-upload">
      <div class="upload-area" @click="triggerInput">
        <el-icon class="upload-icon" :size="40"><UploadFilled /></el-icon>
        <p class="upload-text">点击选择多张图片</p>
        <p class="upload-hint">使用模板重命名，{num} 为序号占位符</p>
      </div>
      <input ref="fileInput" type="file" accept="image/*" multiple hidden @change="handleFiles" />
      <div v-if="files.length" class="file-list">
        <el-tag v-for="(f, i) in files" :key="i" closable @close="files.splice(i, 1)">{{ f.name }}</el-tag>
      </div>
    </div>

    <div class="tool-params">
      <div class="param-row">
        <span class="param-label">命名模板</span>
        <el-input v-model="params.pattern" placeholder="photo_{num}" size="small" style="width: 220px" />
      </div>
      <div class="param-row">
        <span class="param-label">起始序号</span>
        <el-input-number v-model="params.start" :min="0" :max="9999" size="small" />
        <span class="param-label">补零位数</span>
        <el-input-number v-model="params.padding" :min="1" :max="6" size="small" />
      </div>
    </div>

    <div v-if="files.length" class="tool-actions">
      <el-button type="primary" size="large" round :loading="processing" @click="handleProcess">
        {{ processing ? '处理中...' : `重命名 ${files.length} 个文件` }}
      </el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="resultUrl" class="tool-result">
      <el-result icon="success" title="重命名完成">
        <template #extra>
          <el-button type="success" size="large" round @click="handleDownload">下载 zip 包</el-button>
        </template>
      </el-result>
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
const params = reactive({ pattern: 'photo_{num}', start: 1, padding: 3 })

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
    const res = await api.post('/batch-rename/process', fd, { responseType: 'blob' })
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '重命名失败'
  } finally { processing.value = false }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a'); a.href = url; a.download = 'renamed.zip'; a.click()
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
.param-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.tool-result { margin-top: 8px; }
</style>
