<template>
  <ToolPage module="watermark-add" :params="params">
    <template #params>
      <div class="param-group">
        <label class="param-label">水印类型</label>
        <el-radio-group v-model="params.type">
          <el-radio-button value="text">文字水印</el-radio-button>
          <el-radio-button value="image">图片水印</el-radio-button>
        </el-radio-group>
      </div>

      <template v-if="params.type === 'text'">
        <div class="param-group">
          <label class="param-label">水印文字</label>
          <el-input v-model="params.text" placeholder="输入水印文字" />
        </div>
        <div class="param-group">
          <label class="param-label">字体大小</label>
          <el-input-number v-model="params.font_size" :min="8" :max="200" />
        </div>
      </template>

      <div class="param-group">
        <label class="param-label">位置</label>
        <el-select v-model="params.position" style="width: 100%">
          <el-option label="左上角" value="top-left" />
          <el-option label="右上角" value="top-right" />
          <el-option label="左下角" value="bottom-left" />
          <el-option label="右下角" value="bottom-right" />
          <el-option label="居中" value="center" />
        </el-select>
      </div>

      <div class="param-group">
        <label class="param-label">不透明度</label>
        <el-slider v-model="params.opacity" :min="0.1" :max="1" :step="0.05" show-input />
      </div>

      <template v-if="params.type === 'text'">
        <div class="param-row">
          <label>文字颜色</label>
          <el-color-picker v-model="params.color" />
        </div>
      </template>
      <template v-else>
        <div class="param-group">
          <label class="param-label">水印缩放</label>
          <el-slider v-model="params.scale" :min="0.05" :max="0.5" :step="0.01" show-input />
        </div>
      </template>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive<Record<string, unknown>>({
  type: 'text',
  text: 'Watermark',
  font_size: 36,
  position: 'bottom-right',
  opacity: 0.5,
  color: '#ffffff',
  scale: 0.15,
})
</script>

<style scoped>
.param-group {
  margin-top: 16px;
}
.param-group:first-child {
  margin-top: 4px;
}
.param-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}
.param-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid var(--border-color);
  margin-top: 16px;
}
.param-row label {
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
