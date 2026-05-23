<template>
  <div class="tool-page">
    <div class="preset-header">
      <h2>处理预设管理</h2>
      <el-button type="primary" @click="showSave = true" :icon="Plus">新建预设</el-button>
    </div>

    <div v-if="loading" class="loading-box">
      <el-skeleton :rows="4" animated />
    </div>

    <div v-if="errorMsg" class="tool-error">
      <el-alert :title="errorMsg" type="error" show-icon closable @close="errorMsg = ''" />
    </div>

    <div v-if="!loading && presets.length === 0" class="empty-box">
      <el-empty description="暂无预设，保存任意工具的参数即可创建" />
    </div>

    <div v-if="presets.length" class="preset-grid">
      <el-card v-for="p in presets" :key="p.id" class="preset-card">
        <div class="preset-info">
          <h4>{{ p.name }}</h4>
          <el-tag size="small">{{ p.module }}</el-tag>
        </div>
        <div class="preset-params">
          <code>{{ JSON.stringify(p.params) }}</code>
        </div>
        <div class="preset-actions">
          <el-button size="small" type="danger" text @click="deletePreset(p.id)">删除</el-button>
        </div>
      </el-card>
    </div>

    <el-dialog v-model="showSave" title="保存预设" width="420px">
      <el-form label-position="top">
        <el-form-item label="名称">
          <el-input v-model="form.name" placeholder="如：小红书发布" />
        </el-form-item>
        <el-form-item label="模块">
          <el-input v-model="form.module" placeholder="如：social-media" />
        </el-form-item>
        <el-form-item label="参数 JSON">
          <el-input v-model="form.paramsJson" type="textarea" :rows="5" placeholder='{"platform": "xiaohongshu"}' />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSave = false">取消</el-button>
        <el-button type="primary" @click="savePreset">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

interface Preset { id: string; name: string; module: string; params: Record<string, unknown> }

const presets = ref<Preset[]>([])
const loading = ref(false)
const errorMsg = ref('')
const showSave = ref(false)
const form = reactive({ name: '', module: '', paramsJson: '{}' })

async function loadPresets() {
  loading.value = true
  try {
    const res = await api.get('/preset-save/list')
    presets.value = res.data.presets ?? []
  } catch (e: any) {
    errorMsg.value = '加载预设失败'
  } finally { loading.value = false }
}

async function savePreset() {
  try {
    const params = JSON.parse(form.paramsJson)
    const fd = new FormData()
    fd.append('params', JSON.stringify({ name: form.name, module: form.module, params }))
    await api.post('/preset-save/save', fd)
    ElMessage.success('预设已保存')
    showSave.value = false
    form.name = ''; form.module = ''; form.paramsJson = '{}'
    loadPresets()
  } catch (e: any) {
    if (e instanceof SyntaxError) {
      ElMessage.error('JSON 格式错误')
    } else {
      errorMsg.value = e?.response?.data?.detail || '保存失败'
    }
  }
}

async function deletePreset(id: string) {
  try {
    const fd = new FormData()
    fd.append('params', JSON.stringify({ id }))
    await api.post('/preset-save/delete', fd)
    ElMessage.success('已删除')
    loadPresets()
  } catch (e: any) {
    errorMsg.value = '删除失败'
  }
}

onMounted(loadPresets)
</script>

<style scoped>
.tool-page { max-width: 800px; margin: 0 auto; }
.preset-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.preset-header h2 { margin: 0; font-size: 20px; }
.loading-box { background: var(--card-bg); padding: 24px; border-radius: var(--radius); }
.tool-error { margin-bottom: 24px; }
.empty-box { background: var(--card-bg); border-radius: var(--radius); padding: 20px; }
.preset-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
.preset-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.preset-info h4 { margin: 0; font-size: 15px; }
.preset-params { background: #f5f7fa; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; overflow-x: auto; }
.preset-params code { font-size: 12px; color: #606266; white-space: pre; }
.preset-actions { text-align: right; }
</style>
