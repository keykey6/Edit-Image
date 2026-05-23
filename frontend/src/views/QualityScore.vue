<template>
  <div class="tool-page">
    <div class="tool-upload">
      <ImageUploader v-model="file" />
    </div>

    <div v-if="file" class="tool-actions">
      <el-button type="primary" size="large" round :loading="loading" @click="evaluate">评估质量</el-button>
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="result" class="result-panel">
      <div class="score-ring">
        <el-progress type="dashboard" :percentage="result.overall_score" :color="scoreColor" :width="180">
          <template #default="{ percentage }">
            <span class="score-value">{{ percentage }}</span>
          </template>
        </el-progress>
        <el-tag :type="levelTag" size="large" class="level-tag">{{ result.level }}</el-tag>
      </div>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-value">{{ result.sharpness }}</div>
          <div class="metric-label">清晰度</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ result.noise }}</div>
          <div class="metric-label">噪点水平</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ result.color_richness }}</div>
          <div class="metric-label">色彩丰富度</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import api from '@/api'
import ImageUploader from '@/components/ImageUploader.vue'

const file = ref<File | null>(null)
const loading = ref(false)
const errorMsg = ref('')
const result = ref<any>()

const scoreColor = computed(() => {
  if (!result.value) return '#6C5CE7'
  const s = result.value.overall_score
  if (s >= 70) return '#67c23a'
  if (s >= 40) return '#e6a23c'
  return '#f56c6c'
})

const levelTag = computed(() => {
  const level = result.value?.level ?? ''
  if (level.includes('优秀') || level.includes('excellent')) return 'success'
  if (level.includes('良好') || level.includes('good')) return ''
  if (level.includes('一般') || level.includes('average')) return 'warning'
  return 'danger'
})

async function evaluate() {
  if (!file.value) return
  loading.value = true; errorMsg.value = ''
  try {
    const fd = new FormData()
    fd.append('file', file.value)
    const res = await api.post('/quality-score/process', fd)
    result.value = res.data
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || e?.message || '评估失败'
  } finally { loading.value = false }
}
</script>

<style scoped>
.tool-page { max-width: 700px; margin: 0 auto; }
.tool-upload { margin-bottom: 24px; }
.tool-actions { text-align: center; margin-bottom: 24px; }
.tool-error { margin-bottom: 24px; }
.result-panel { background: var(--card-bg); border-radius: var(--radius); padding: 32px; box-shadow: var(--shadow); }
.score-ring { text-align: center; margin-bottom: 28px; }
.score-value { font-size: 28px; font-weight: 700; }
.level-tag { margin-top: 12px; }
.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.metric-card { text-align: center; padding: 16px; background: var(--bg-color); border-radius: 12px; }
.metric-value { font-size: 24px; font-weight: 700; color: var(--primary); }
.metric-label { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
</style>
