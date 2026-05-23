<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div class="tool-params">
      <div class="param-group">
        <label class="param-label">证件照规格</label>
        <el-select v-model="params.size" style="width: 100%">
          <el-option label="一寸 (25 x 35 mm)" value="1inch" />
          <el-option label="小一寸 (22 x 32 mm)" value="small1inch" />
          <el-option label="二寸 (35 x 49 mm)" value="2inch" />
          <el-option label="小二寸 (35 x 45 mm)" value="small2inch" />
          <el-option label="大一寸 (33 x 48 mm)" value="large1inch" />
        </el-select>
      </div>

      <div class="param-group">
        <label class="param-label">背景颜色</label>
        <div class="color-options">
          <button
            v-for="c in bgColors"
            :key="c.value"
            :class="{ active: params.bg === c.value }"
            :style="{ background: c.hex }"
            @click="params.bg = c.value"
          />
          <span class="color-name">{{ bgColors.find(c => c.value === params.bg)?.label }}</span>
        </div>
      </div>

      <div class="param-row">
        <label>打印排版（包含多张照片）</label>
        <el-switch v-model="params.layout" active-value="grid" inactive-value="single" />
      </div>
    </div>

    <div v-if="file" class="tool-actions">
      <el-button type="primary" size="large" round :loading="processing" @click="handleProcess">
        <el-icon v-if="!processing"><Camera /></el-icon>
        {{ processing ? '处理中...' : '生成证件照' }}
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
          下载证件照
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
const processing = ref(false)
const errorMsg = ref('')
const resultUrl = ref<string>()
const resultBlob = ref<Blob>()

const params = reactive<Record<string, unknown>>({
  size: '1inch',
  bg: 'white',
  layout: 'single',
})

const bgColors = [
  { value: 'white', label: '白色', hex: '#ffffff' },
  { value: 'red', label: '红色', hex: '#d32f2f' },
  { value: 'blue', label: '蓝色', hex: '#1976d2' },
]

const originalUrl = computed(() => file.value ? URL.createObjectURL(file.value) : undefined)

async function handleProcess() {
  if (!file.value) return
  processing.value = true
  errorMsg.value = ''
  try {
    const formData = new FormData()
    formData.append('file', file.value)
    formData.append('params', JSON.stringify(params))
    const res = await api.post('/id-photo/process', formData, { responseType: 'blob' })
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
  a.download = 'id_photo.png'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.tool-page { max-width: 900px; margin: 0 auto; }
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
.color-options { display: flex; gap: 12px; align-items: center; }
.color-options button {
  width: 36px; height: 36px; border-radius: 50%;
  border: 3px solid transparent; cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}
.color-options button:hover { transform: scale(1.15); }
.color-options button.active {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(108, 92, 231, 0.2);
}
.color-name { font-size: 14px; color: var(--text-primary); margin-left: 4px; }
.param-row {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 16px; margin-top: 16px;
  border-top: 1px solid var(--border-color);
}
.param-row label { font-size: 13px; color: var(--text-secondary); }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.tool-result { margin-top: 8px; }
.tool-download { text-align: center; margin-top: 24px; }
</style>
