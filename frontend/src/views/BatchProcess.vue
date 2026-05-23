<template>
  <div class="tool-page">
    <div class="tool-upload">
      <div class="upload-area" @click="triggerInput">
        <el-icon class="upload-icon" :size="40"><UploadFilled /></el-icon>
        <p class="upload-text">点击选择多张图片</p>
        <p class="upload-hint">支持 JPG / PNG / WebP，最大 20MB</p>
      </div>
      <input ref="fileInput" type="file" accept="image/*" multiple hidden @change="handleFiles" />
      <div v-if="files.length" class="file-list">
        <el-tag
          v-for="(f, i) in files"
          :key="i"
          closable
          @close="files.splice(i, 1)"
        >
          {{ f.name }}
        </el-tag>
      </div>
    </div>

    <div class="tool-params">
      <div class="param-group">
        <label class="param-label">处理操作</label>
        <el-select v-model="params.operation" style="width: 100%">
          <el-option label="压缩" value="compress" />
          <el-option label="缩放" value="resize" />
          <el-option label="格式转换" value="format_convert" />
          <el-option label="灰度化" value="grayscale" />
          <el-option label="水平翻转" value="flip_h" />
          <el-option label="垂直翻转" value="flip_v" />
        </el-select>
      </div>

      <template v-if="params.operation === 'compress'">
        <ParamSlider v-model="params.quality" label="压缩质量" :min="1" :max="100" />
        <div class="param-group">
          <label class="param-label">最大尺寸 (0=不限制)</label>
          <el-input-number v-model="params.max_size" :min="0" :max="10000" :step="100" />
        </div>
      </template>
      <template v-if="params.operation === 'resize'">
        <div class="param-row">
          <div class="param-item">
            <label class="param-label">宽度</label>
            <el-input-number v-model="params.width" :min="1" :max="10000" />
          </div>
          <div class="param-item">
            <label class="param-label">高度</label>
            <el-input-number v-model="params.height" :min="1" :max="10000" />
          </div>
        </div>
      </template>
      <template v-if="params.operation === 'format_convert'">
        <div class="param-group">
          <label class="param-label">输出格式</label>
          <el-select v-model="params.output_format" style="width: 200px">
            <el-option label="保持原格式" value="original" />
            <el-option label="PNG" value="png" />
            <el-option label="JPEG" value="jpg" />
            <el-option label="WebP" value="webp" />
          </el-select>
        </div>
      </template>
    </div>

    <div v-if="files.length" class="tool-actions">
      <el-button type="primary" size="large" round :loading="processing" @click="handleProcess">
        <el-icon v-if="!processing"><List /></el-icon>
        {{ processing ? '处理中...' : `处理 ${files.length} 张图片` }}
      </el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="resultUrl" class="tool-result">
      <el-result icon="success" title="批量处理完成">
        <template #extra>
          <el-button type="success" size="large" round @click="handleDownload">
            <el-icon><Download /></el-icon>
            下载 zip 包
          </el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import api from '@/api'
import ParamSlider from '@/components/ParamSlider.vue'

const files = ref<File[]>([])
const fileInput = ref<HTMLInputElement>()
const processing = ref(false)
const errorMsg = ref('')
const resultUrl = ref<string>()
const resultBlob = ref<Blob>()

const params = reactive<Record<string, unknown>>({
  operation: 'compress',
  quality: 70,
  max_size: 0,
  width: 800,
  height: 600,
  output_format: 'original',
})

function triggerInput() {
  fileInput.value?.click()
}

function handleFiles(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files) {
    files.value = Array.from(input.files)
  }
}

async function handleProcess() {
  if (!files.value.length) return
  processing.value = true
  errorMsg.value = ''
  try {
    const formData = new FormData()
    for (const f of files.value) {
      formData.append('files', f)
    }
    formData.append('params', JSON.stringify(params))
    const res = await api.post('/batch-process/process', formData, { responseType: 'blob' })
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '处理失败'
  } finally {
    processing.value = false
  }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a')
  a.href = url
  a.download = 'batch_processed.zip'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.tool-page { max-width: 900px; margin: 0 auto; }
.tool-upload { margin-bottom: 24px; }
.upload-area {
  border: 2px dashed var(--border-color);
  border-radius: var(--radius);
  padding: 36px 24px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s, background 0.3s;
}
.upload-area:hover {
  border-color: var(--primary);
  background: rgba(108, 92, 231, 0.04);
}
.upload-icon { color: var(--primary-light); margin-bottom: 12px; }
.upload-text { font-size: 15px; color: var(--text-primary); margin-bottom: 6px; }
.upload-hint { font-size: 12px; color: var(--text-secondary); }
.file-list { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
.tool-params {
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: var(--shadow);
}
.param-group { margin-top: 16px; }
.param-group:first-child { margin-top: 0; }
.param-label { display: block; font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; }
.param-row { display: flex; gap: 24px; }
.param-item { display: flex; flex-direction: column; gap: 6px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.tool-result { margin-top: 8px; }
</style>
