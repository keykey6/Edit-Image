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
        <button
          class="btn-primary"
          :disabled="processing"
          @click="handleProcess"
        >
          <el-icon v-if="!processing" :size="18"><MagicStick /></el-icon>
          <span v-else class="btn-spinner" />
          {{ processing ? '处理中…' : '开始处理' }}
        </button>
      </div>
    </div>

    <div v-if="file && !$slots.params" class="tool-action-only">
      <button
        class="btn-primary"
        :disabled="processing"
        @click="handleProcess"
      >
        <el-icon v-if="!processing" :size="18"><MagicStick /></el-icon>
        <span v-else class="btn-spinner" />
        {{ processing ? '处理中…' : '开始处理' }}
      </button>
    </div>

    <div v-if="processing" class="tool-progress">
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: progressPct + '%' }" />
      </div>
      <p class="progress-hint">正在处理图片，请稍候…</p>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <div class="error-glass">
        <el-icon :size="18" class="error-icon"><WarningFilled /></el-icon>
        <span>{{ errorMsg }}</span>
        <button class="error-close" @click="errorMsg = ''">
          <el-icon :size="14"><Close /></el-icon>
        </button>
      </div>
    </div>

    <div v-if="!processing && originalUrl && resultUrl" class="tool-result">
      <ImageCompare :original="originalUrl" :processed="resultUrl" />
      <div class="result-actions">
        <button class="btn-primary" @click="handleDownload">
          <el-icon :size="16"><Download /></el-icon>
          下载结果
        </button>
        <button class="btn-secondary" @click="handleReset">
          <el-icon :size="16"><Refresh /></el-icon>
          重新处理
        </button>
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
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  padding: 24px;
  margin-bottom: 24px;
}
.bar-params {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--divider);
}
.bar-action { text-align: center; }

/* Action only (no params slot) */
.tool-action-only { text-align: center; margin-bottom: 24px; }

/* Buttons */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: 0 4px 16px rgba(123, 97, 255, 0.35);
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(123, 97, 255, 0.45);
}
.btn-primary:active:not(:disabled) {
  transform: scale(0.97);
}
.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  color: var(--text-secondary);
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition);
}
.btn-secondary:hover {
  border-color: var(--primary-light);
  color: var(--primary);
  background: rgba(123, 97, 255, 0.06);
}

.btn-spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Progress */
.tool-progress { margin-bottom: 24px; }
.progress-track {
  height: 4px;
  background: var(--border-light);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-light));
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}
.progress-hint {
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-muted);
  text-align: center;
}

/* Error */
.tool-error { margin-bottom: 24px; }
.error-glass {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: rgba(239, 68, 68, 0.08);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: var(--radius);
  color: #DC2626;
  font-size: 13px;
  font-weight: 500;
}
.error-icon { flex-shrink: 0; }
.error-close {
  margin-left: auto;
  width: 24px; height: 24px;
  border: none;
  background: none;
  color: #DC2626;
  cursor: pointer;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition-fast);
}
.error-close:hover { background: rgba(239, 68, 68, 0.1); }

/* Result */
.tool-result { margin-top: 8px; }
.result-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 28px;
}
</style>
