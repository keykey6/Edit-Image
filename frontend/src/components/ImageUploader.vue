<template>
  <div
    class="uploader"
    :class="{ 'is-dragover': dragover, 'has-file': modelValue }"
    @dragover.prevent="dragover = true"
    @dragleave.prevent="dragover = false"
    @drop.prevent="handleDrop"
    @paste="handlePaste"
    tabindex="0"
  >
    <input
      ref="inputRef"
      type="file"
      accept="image/*"
      :multiple="multiple"
      hidden
      @change="handleChange"
    />
    <div class="uploader-inner" @click="inputRef?.click()">
      <template v-if="!modelValue">
        <div class="upload-icon-wrap">
          <el-icon class="upload-icon" :size="36"><UploadFilled /></el-icon>
        </div>
        <p class="upload-text">拖拽图片到此处，或 <span>点击上传</span></p>
        <p class="upload-hint">
          <kbd>Ctrl+V</kbd> 粘贴 · JPG / PNG / WebP · 最大 20MB
        </p>
      </template>
      <template v-else>
        <div class="preview-area">
          <img v-if="previewUrl" :src="previewUrl" alt="preview" />
          <div class="preview-overlay">
            <el-icon :size="20"><Refresh /></el-icon>
            <span>点击更换图片</span>
          </div>
        </div>
      </template>
    </div>
    <button v-if="modelValue" class="clear-btn" @click.stop="clearFile" title="移除">
      <el-icon :size="16"><Close /></el-icon>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: File | null
  multiple?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [file: File | null]
}>()

const dragover = ref(false)
const inputRef = ref<HTMLInputElement>()
const previewUrl = ref<string>()

watch(() => props.modelValue, (file) => {
  if (file) { previewUrl.value = URL.createObjectURL(file) }
  else { previewUrl.value = undefined }
})

function handleDrop(e: DragEvent) {
  dragover.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file && file.type.startsWith('image/')) emit('update:modelValue', file)
}

function handleChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) emit('update:modelValue', file)
}

function handlePaste(e: ClipboardEvent) {
  const items = e.clipboardData?.items
  if (!items) return
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile()
      if (file) { emit('update:modelValue', file); break }
    }
  }
}

function clearFile() {
  if (inputRef.value) inputRef.value.value = ''
  emit('update:modelValue', null)
}
</script>

<style scoped>
.uploader {
  position: relative;
  border: 2px dashed var(--border-color);
  border-radius: var(--radius);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
  outline: none;
}
.uploader:focus-visible { border-color: var(--primary-light); }
.uploader:hover, .uploader.is-dragover {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.uploader.is-dragover {
  border-style: solid;
  box-shadow: 0 0 0 4px rgba(108, 92, 231, 0.12);
}
.uploader.has-file {
  border-style: solid;
  border-color: var(--border-color);
  padding: 0;
}

.uploader-inner { padding: 44px 24px; text-align: center; }

.upload-icon-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px; height: 64px;
  background: var(--primary-bg);
  border-radius: 16px;
  margin-bottom: 16px;
}
.upload-icon { color: var(--primary); }

.upload-text { font-size: 15px; color: var(--text-primary); margin-bottom: 8px; }
.upload-text span { color: var(--primary); font-weight: 600; }

.upload-hint { font-size: 12px; color: var(--text-muted); display: flex; align-items: center; justify-content: center; gap: 8px; }
.upload-hint kbd {
  display: inline-block;
  padding: 1px 6px;
  font-size: 11px;
  font-family: inherit;
  color: var(--text-secondary);
  background: var(--content-bg);
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.preview-area {
  position: relative;
  border-radius: var(--radius);
  overflow: hidden;
}
.preview-area img {
  display: block;
  width: 100%;
  max-height: 320px;
  object-fit: contain;
  background: #f1f5f9;
}
.preview-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #fff;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.2s;
}
.preview-area:hover .preview-overlay { opacity: 1; }

.clear-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 28px; height: 28px;
  border: none;
  background: rgba(0,0,0,0.5);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 2;
  transition: background 0.2s;
}
.clear-btn:hover { background: #e74c3c; }
</style>
