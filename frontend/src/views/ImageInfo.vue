<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div v-if="file && !loading" class="tool-actions">
      <el-button type="primary" size="large" round @click="handleCheck">
        <el-icon><Search /></el-icon>
        查看图片信息
      </el-button>
    </div>

    <div v-if="loading" class="loading-area">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <p>正在读取...</p>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="info" class="info-card">
      <el-descriptions :column="2" border size="large">
        <el-descriptions-item label="文件名">{{ info.filename }}</el-descriptions-item>
        <el-descriptions-item label="格式">{{ info.format }}</el-descriptions-item>
        <el-descriptions-item label="尺寸">{{ info.width }} x {{ info.height }} px</el-descriptions-item>
        <el-descriptions-item label="宽高比">{{ info.aspect_ratio }}</el-descriptions-item>
        <el-descriptions-item label="文件大小">{{ info.file_size }}</el-descriptions-item>
        <el-descriptions-item label="模式">{{ info.mode }}</el-descriptions-item>
        <el-descriptions-item v-if="info.exif" label="EXIF" :span="2">
          <pre>{{ info.exif }}</pre>
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'
import ImageUploader from '@/components/ImageUploader.vue'

const file = ref<File | null>(null)
const loading = ref(false)
const errorMsg = ref('')
const info = ref<any>(null)

async function handleCheck() {
  if (!file.value) return
  loading.value = true
  errorMsg.value = ''
  info.value = null
  try {
    const formData = new FormData()
    formData.append('file', file.value)
    const res = await api.post('/image-info/process', formData)
    info.value = res.data
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '读取失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.tool-page {
  max-width: 900px;
  margin: 0 auto;
}
.tool-upload { margin-bottom: 24px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.loading-area { text-align: center; padding: 40px; color: var(--text-secondary); }
.loading-area p { margin-top: 12px; }
.tool-error { margin-bottom: 24px; }
.info-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
}
pre {
  white-space: pre-wrap;
  font-size: 12px;
  color: var(--text-secondary);
  max-height: 200px;
  overflow-y: auto;
}
</style>
