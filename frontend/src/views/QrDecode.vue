<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div v-if="file" class="tool-actions">
      <el-button type="primary" size="large" round :loading="loading" @click="decode">识别二维码</el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="result" class="result-panel">
      <div v-if="result.decoded && result.decoded.length" class="decode-list">
        <h3>识别结果</h3>
        <el-card v-for="(item, i) in result.decoded" :key="i" class="decode-card">
          <div class="decode-type">
            <el-tag size="small">{{ item.type }}</el-tag>
          </div>
          <div class="decode-data">{{ item.data }}</div>
          <div v-if="item.rect" class="decode-rect">
            位置: ({{ item.rect.x }}, {{ item.rect.y }}) {{ item.rect.w }}×{{ item.rect.h }}
          </div>
        </el-card>
      </div>
      <el-empty v-else description="未识别到二维码或条形码" />
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
const result = ref<any>()

async function decode() {
  if (!file.value) return
  loading.value = true; errorMsg.value = ''
  try {
    const fd = new FormData()
    fd.append('file', file.value)
    const res = await api.post('/qr-decode/process', fd)
    result.value = res.data
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '识别失败'
  } finally { loading.value = false }
}
</script>

<style scoped>
.tool-page { max-width: 700px; margin: 0 auto; }
.tool-upload { margin-bottom: 24px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.result-panel { background: var(--card-bg); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); }
.result-panel h3 { margin: 0 0 16px 0; }
.decode-list { display: flex; flex-direction: column; gap: 12px; }
.decode-type { margin-bottom: 8px; }
.decode-data { font-size: 16px; font-weight: 600; word-break: break-all; margin-bottom: 6px; }
.decode-rect { font-size: 12px; color: var(--text-secondary); }
</style>
