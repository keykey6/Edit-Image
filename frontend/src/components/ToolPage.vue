<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div v-if="file && $slots.params" class="tool-bar">
      <div class="bar-params">
        <slot name="params" />
      </div>
      <div class="bar-action">
        <el-button
          type="primary"
          size="large"
          round
          :loading="processing"
          @click="handleProcess"
        >
          <el-icon v-if="!processing"><MagicStick /></el-icon>
          {{ processing ? '处理中…' : '开始处理' }}
        </el-button>
      </div>
    </div>

    <div v-if="file && !$slots.params" class="tool-action-only">
      <el-button
        type="primary"
        size="large"
        round
        :loading="processing"
        @click="handleProcess"
      >
        <el-icon v-if="!processing"><MagicStick /></el-icon>
        {{ processing ? '处理中…' : '开始处理' }}
      </el-button>
    </div>

    <div v-if="processing" class="tool-progress">
      <el-progress :percentage="progressPct" :stroke-width="4" :show-text="false" />
      <p class="progress-hint">正在处理图片，请稍候…</p>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="!processing && originalUrl && resultUrl" class="tool-result">
      <ImageCompare :original="originalUrl" :processed="resultUrl" />
      <div class="result-actions">
        <el-button type="primary" size="large" round @click="handleDownload">
          <el-icon><Download /></el-icon>
          下载结果
        </el-button>
        <el-button size="large" round @click="handleReset">
          <el-icon><Refresh /></el-icon>
          重新处理
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import api from '@/api'
import ImageUploader from '@/components/ImageUploader.vue'
import ImageCompare from '@/components/ImageCompare.vue'

const props = defineProps<{
  module: string
  params?: Record<string, unknown>
}>()

const file = ref<File | null>(null)
const processing = ref(false)
const errorMsg = ref('')
const resultUrl = ref<string>()
const resultBlob = ref<Blob>()
const progressPct = ref(0)

let progressTimer: ReturnType<typeof setInterval> | null = null

const originalUrl = computed(() => {
  if (!file.value) return undefined
  return URL.createObjectURL(file.value)
})

watch(file, () => {
  resultUrl.value = undefined
  resultBlob.value = undefined
  errorMsg.value = ''
})

async function handleProcess() {
  if (!file.value) return
  processing.value = true
  errorMsg.value = ''
  progressPct.value = 0
  startProgress()

  try {
    const formData = new FormData()
    formData.append('file', file.value)
    if (props.params && Object.keys(props.params).length > 0) {
      formData.append('params', JSON.stringify(props.params))
    }
    const res = await api.post(
      `/${props.module}/process`,
      formData,
      { responseType: 'blob' }
    )
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '处理失败，请重试'
  } finally {
    stopProgress()
    progressPct.value = 100
    processing.value = false
  }
}

function startProgress() {
  progressPct.value = 20
  progressTimer = setInterval(() => {
    if (progressPct.value < 90) progressPct.value += 3
  }, 400)
}

function stopProgress() {
  if (progressTimer) { clearInterval(progressTimer); progressTimer = null }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a')
  a.href = url
  const ext = resultBlob.value.type.includes('zip') ? 'zip' : 'png'
  a.download = `${props.module}_result.${ext}`
  a.click()
  URL.revokeObjectURL(url)
}

function handleReset() {
  resultUrl.value = undefined
  resultBlob.value = undefined
}
</script>

<style scoped>
.tool-page { max-width: 900px; margin: 0 auto; }

.tool-upload { margin-bottom: 24px; }

/* Toolbar for params + action */
.tool-bar {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px 24px;
  margin-bottom: 24px;
}
.bar-params {
  margin-bottom: 18px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--border-color);
}
.bar-action { text-align: center; }

/* Action only (no params slot) */
.tool-action-only { text-align: center; margin-bottom: 24px; }

.tool-progress { margin-bottom: 24px; }
.progress-hint {
  margin-top: 8px;
  font-size: 13px;
  color: var(--text-muted);
  text-align: center;
}

.tool-error { margin-bottom: 24px; }

.tool-result { margin-top: 8px; }
.result-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}
</style>
