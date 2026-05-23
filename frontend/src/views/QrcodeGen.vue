<template>
  <div class="tool-page">
    <div class="qr-form">
      <div class="param-group">
        <label class="param-label">二维码内容 (URL / 文本)</label>
        <el-input
          v-model="params.text"
          type="textarea"
          :rows="3"
          placeholder="输入网址或文本内容"
        />
      </div>

      <div class="param-row">
        <div class="param-item">
          <label>尺寸</label>
          <el-input-number v-model="params.size" :min="100" :max="1000" :step="50" />
        </div>
        <div class="param-item">
          <label>前景色</label>
          <el-color-picker v-model="params.fg_color" />
        </div>
        <div class="param-item">
          <label>背景色</label>
          <el-color-picker v-model="params.bg_color" />
        </div>
      </div>

      <div class="tool-actions">
        <el-button type="primary" size="large" round :loading="loading" @click="handleGenerate">
          <el-icon v-if="!loading"><Postcard /></el-icon>
          {{ loading ? '生成中...' : '生成二维码' }}
        </el-button>
      </div>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="resultUrl" class="qr-result">
      <img :src="resultUrl" alt="QR Code" />
      <el-button type="success" size="large" round @click="handleDownload">
        <el-icon><Download /></el-icon>
        下载二维码
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import api from '@/api'

const params = reactive<Record<string, unknown>>({
  text: 'https://example.com',
  size: 300,
  fg_color: '#000000',
  bg_color: '#ffffff',
})

const loading = ref(false)
const errorMsg = ref('')
const resultUrl = ref<string>()
const resultBlob = ref<Blob>()

async function handleGenerate() {
  loading.value = true
  errorMsg.value = ''
  try {
    const formData = new FormData()
    formData.append('params', JSON.stringify(params))
    const res = await api.post('/qrcode-gen/process', formData, { responseType: 'blob' })
    resultBlob.value = res.data
    if (resultUrl.value) URL.revokeObjectURL(resultUrl.value)
    resultUrl.value = URL.createObjectURL(res.data)
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '生成失败'
  } finally {
    loading.value = false
  }
}

function handleDownload() {
  if (!resultBlob.value) return
  const url = URL.createObjectURL(resultBlob.value)
  const a = document.createElement('a')
  a.href = url
  a.download = 'qrcode.png'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.tool-page {
  max-width: 700px;
  margin: 0 auto;
}
.qr-form {
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
}
.param-group { margin-bottom: 20px; }
.param-label { display: block; font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; }
.param-row { display: flex; gap: 24px; align-items: flex-end; margin-bottom: 20px; }
.param-item { display: flex; flex-direction: column; gap: 6px; }
.param-item label { font-size: 12px; color: var(--text-secondary); }
.tool-actions { text-align: center; }
.tool-error { margin-top: 24px; }
.qr-result { text-align: center; margin-top: 32px; }
.qr-result img { max-width: 300px; border-radius: 12px; box-shadow: var(--shadow); margin-bottom: 20px; }
</style>
