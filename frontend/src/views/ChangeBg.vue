<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div class="tool-params">
      <div class="param-group">
        <label class="param-label">背景类型</label>
        <el-radio-group v-model="mode">
          <el-radio-button value="color">纯色背景</el-radio-button>
          <el-radio-button value="image">图片背景</el-radio-button>
        </el-radio-group>
      </div>

      <div v-if="mode === 'color'" class="param-row">
        <label>背景颜色</label>
        <el-color-picker v-model="params.bg_color" />
      </div>
      <div v-else class="param-group">
        <label class="param-label">上传背景图片</label>
        <input type="file" accept="image/*" @change="handleBgFile" />
      </div>
    </div>

    <div class="tool-actions">
      <el-button type="primary" size="large" round :loading="processing" @click="handleProcess">
        <el-icon v-if="!processing"><MagicStick /></el-icon>
        {{ processing ? '处理中...' : '开始换背景' }}
      </el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="originalUrl && resultUrl" class="tool-result">
      <ImageCompare :original="originalUrl" :processed="resultUrl" />
      <div class="tool-download">
        <el-button type="success" size="large" round @click="handleDownload">
          <el-icon><Download /></el-icon>
          下载结果
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import api from '@/api'
import ImageUploader from '@/components/ImageUploader.vue'
import ImageCompare from '@/components/ImageCompare.vue'

const file = ref<File | null>(null)
const bgFile = ref<File | null>(null)
const mode = ref('color')
const processing = ref(false)
const errorMsg = ref('')
const resultUrl = ref<string>()
const resultBlob = ref<Blob>()

const params = reactive<Record<string, unknown>>({
  bg_color: '#ff0000',
})

const originalUrl = computed(() => file.value ? URL.createObjectURL(file.value) : undefined)

function handleBgFile(e: Event) {
  const input = e.target as HTMLInputElement
  bgFile.value = input.files?.[0] || null
}

async function handleProcess() {
  if (!file.value) return
  processing.value = true
  errorMsg.value = ''
  try {
    const formData = new FormData()
    formData.append('file', file.value)
    if (mode.value === 'image' && bgFile.value) {
      formData.append('bg_file', bgFile.value)
    }
    formData.append('params', JSON.stringify({ bg_color: params.bg_color }))
    const res = await api.post('/change-bg/process', formData, { responseType: 'blob' })
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '处理失败，请重试'
  } finally {
    processing.value = false
  }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a')
  a.href = url
  a.download = 'change_bg_result.png'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.tool-page {
  max-width: 900px;
  margin: 0 auto;
}
.tool-upload { margin-bottom: 24px; }
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
.param-row { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
.param-row label { font-size: 13px; color: var(--text-secondary); }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.tool-result { margin-top: 8px; }
.tool-download { text-align: center; margin-top: 24px; }
</style>
