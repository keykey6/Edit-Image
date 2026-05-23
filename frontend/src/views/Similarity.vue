<template>
  <div class="tool-page">
    <div class="dual-upload">
      <div class="upload-box">
        <ImageUploader v-model="file1" />
      </div>
      <div class="upload-box">
        <ImageUploader v-model="file2" />
      </div>
    </div>

    <div class="tool-params">
      <div class="param-row">
        <span class="param-label">算法</span>
        <el-select v-model="method" size="small" style="width: 180px">
          <el-option label="pHash (感知哈希)" value="phash" />
          <el-option label="dHash (差异哈希)" value="dhash" />
          <el-option label="aHash (均值哈希)" value="ahash" />
          <el-option label="wHash (小波哈希)" value="whash" />
        </el-select>
      </div>
    </div>

    <div v-if="file1 && file2" class="tool-actions">
      <el-button type="primary" size="large" round :loading="loading" @click="compare">对比相似度</el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="result" class="result-panel">
      <div class="score-ring">
        <el-progress type="dashboard" :percentage="result.similarity_percent" :color="scoreColor" :width="180">
          <template #default="{ percentage }">
            <span class="score-value">{{ percentage }}%</span>
          </template>
        </el-progress>
        <el-tag :type="result.similar ? 'success' : 'warning'" size="large" class="score-tag">
          {{ result.similar ? '相似' : '不相似' }}
        </el-tag>
      </div>
      <div class="detail-grid">
        <div class="detail-item">
          <span class="detail-label">算法</span>
          <span class="detail-value">{{ result.method }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">汉明距离</span>
          <span class="detail-value">{{ result.hamming_distance }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Hash1</span>
          <span class="detail-value mono">{{ result.hash1 }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Hash2</span>
          <span class="detail-value mono">{{ result.hash2 }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import api from '@/api'
import ImageUploader from '@/components/ImageUploader.vue'

const file1 = ref<File | null>(null)
const file2 = ref<File | null>(null)
const method = ref('phash')
const loading = ref(false)
const errorMsg = ref('')
const result = ref<any>()

const scoreColor = computed(() => {
  if (!result.value) return '#6C5CE7'
  return result.value.similar ? '#67c23a' : '#e6a23c'
})

async function compare() {
  if (!file1.value || !file2.value) return
  loading.value = true; errorMsg.value = ''
  try {
    const fd = new FormData()
    fd.append('file1', file1.value)
    fd.append('file2', file2.value)
    fd.append('params', JSON.stringify({ method: method.value }))
    const res = await api.post('/similarity/process', fd)
    result.value = res.data
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '对比失败'
  } finally { loading.value = false }
}
</script>

<style scoped>
.tool-page { max-width: 900px; margin: 0 auto; }
.dual-upload { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
@media (max-width: 700px) { .dual-upload { grid-template-columns: 1fr; } }
.upload-box { min-width: 0; }
.tool-params { background: var(--card-bg); border-radius: var(--radius); padding: 18px 24px; margin-bottom: 24px; box-shadow: var(--shadow); }
.param-row { display: flex; align-items: center; gap: 12px; }
.param-label { font-weight: 600; font-size: 14px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.result-panel { background: var(--card-bg); border-radius: var(--radius); padding: 32px; box-shadow: var(--shadow); }
.score-ring { text-align: center; margin-bottom: 28px; }
.score-value { font-size: 28px; font-weight: 700; }
.score-tag { margin-top: 12px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.detail-item { display: flex; flex-direction: column; gap: 4px; }
.detail-label { font-size: 12px; color: var(--text-secondary); }
.detail-value { font-size: 14px; font-weight: 600; }
.detail-value.mono { font-family: monospace; font-size: 12px; word-break: break-all; }
</style>
