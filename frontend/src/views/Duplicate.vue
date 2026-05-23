<template>
  <div class="tool-page">
    <div class="tool-upload">
      <div class="upload-area" @click="triggerInput">
        <el-icon class="upload-icon" :size="40"><UploadFilled /></el-icon>
        <p class="upload-text">点击选择多张图片</p>
        <p class="upload-hint">检测重复或高度相似的图片</p>
      </div>
      <input ref="fileInput" type="file" accept="image/*" multiple hidden @change="handleFiles" />
      <div v-if="files.length" class="file-list">
        <el-tag v-for="(f, i) in files" :key="i" closable @close="files.splice(i, 1)">{{ f.name }}</el-tag>
      </div>
    </div>

    <div v-if="files.length >= 2" class="tool-actions">
      <el-button type="primary" size="large" round :loading="loading" @click="detect">检测重复图片</el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="result" class="result-panel">
      <el-result :icon="result.duplicate_count > 0 ? 'warning' : 'success'" :title="`发现 ${result.duplicate_count} 组重复`">
        <template #sub-title>
          共分析 {{ result.total }} 张图片，{{ result.duplicate_count ? '存在重复项' : '未发现重复' }}
        </template>
      </el-result>
      <div v-if="result.groups?.length" class="groups">
        <el-card v-for="(g, i) in result.groups" :key="i" class="group-card">
          <template #header>重复组 #{{ i + 1 }}（{{ g.length }} 张）</template>
          <div class="group-files">
            <el-tag v-for="fn in g" :key="fn" size="small">{{ fn }}</el-tag>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'

const files = ref<File[]>([])
const fileInput = ref<HTMLInputElement>()
const loading = ref(false)
const errorMsg = ref('')
const result = ref<any>()

function triggerInput() { fileInput.value?.click() }
function handleFiles(e: Event) {
  const input = e.target as HTMLInputElement
  if (input.files) files.value = [...files.value, ...Array.from(input.files)]
}

async function detect() {
  loading.value = true; errorMsg.value = ''
  try {
    const fd = new FormData()
    for (const f of files.value) fd.append('files', f)
    const res = await api.post('/duplicate/process', fd)
    result.value = res.data
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '检测失败'
  } finally { loading.value = false }
}
</script>

<style scoped>
.tool-page { max-width: 800px; margin: 0 auto; }
.tool-upload { margin-bottom: 24px; }
.upload-area { border: 2px dashed var(--border-color); border-radius: var(--radius); padding: 36px 24px; text-align: center; cursor: pointer; transition: border-color 0.3s; }
.upload-area:hover { border-color: var(--primary); background: rgba(108, 92, 231, 0.04); }
.upload-icon { color: var(--primary-light); margin-bottom: 12px; }
.upload-text { font-size: 15px; color: var(--text-primary); margin-bottom: 6px; }
.upload-hint { font-size: 12px; color: var(--text-secondary); }
.file-list { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.result-panel { background: var(--card-bg); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); }
.groups { margin-top: 20px; display: flex; flex-direction: column; gap: 12px; }
.group-files { display: flex; gap: 6px; flex-wrap: wrap; }
</style>
