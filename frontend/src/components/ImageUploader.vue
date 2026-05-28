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
        <div class="upload-glow">
          <div class="upload-icon-wrap">
            <el-icon class="upload-icon" :size="32"><UploadFilled /></el-icon>
          </div>
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
            <div class="overlay-icon">
              <el-icon :size="20"><Refresh /></el-icon>
            </div>
            <span>点击更换图片</span>
          </div>
        </div>
      </template>
    </div>
    <button v-if="modelValue" class="clear-btn" @click.stop="clearFile" title="移除">
      <el-icon :size="14"><Close /></el-icon>
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
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition);
  outline: none;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
}
.uploader:focus-visible {
  border-color: var(--primary-light);
}
.uploader:hover, .uploader.is-dragover {
  border-color: var(--primary);
  background: rgba(123, 97, 255, 0.04);
  box-shadow: 0 0 0 4px rgba(123, 97, 255, 0.08), var(--shadow);
}
.uploader.is-dragover {
  border-style: solid;
}
.uploader.has-file {
  border-style: solid;
  border-color: var(--border-color);
  padding: 0;
  background: transparent;
  backdrop-filter: none;
}

.uploader-inner { padding: 48px 24px; text-align: center; }

.upload-glow {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}
.upload-glow::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(123, 97, 255, 0.2), rgba(155, 135, 253, 0.08));
  filter: blur(12px);
  opacity: 0;
  transition: opacity var(--transition);
}
.uploader:hover .upload-glow::before,
.uploader.is-dragover .upload-glow::before {
  opacity: 1;
}

.upload-icon-wrap {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px; height: 64px;
  background: linear-gradient(135deg, rgba(123, 97, 255, 0.1), rgba(155, 135, 253, 0.05));
  border-radius: var(--radius);
  transition: all var(--transition);
}
.uploader:hover .upload-icon-wrap,
.uploader.is-dragover .upload-icon-wrap {
  background: linear-gradient(135deg, rgba(123, 97, 255, 0.15), rgba(155, 135, 253, 0.1));
  transform: scale(1.05);
}

.upload-icon { color: var(--primary); }

.upload-text { font-size: 15px; color: var(--text-primary); margin-bottom: 8px; font-weight: 500; }
.upload-text span { color: var(--primary); font-weight: 600; }

.upload-hint { font-size: 12px; color: var(--text-muted); display: flex; align-items: center; justify-content: center; gap: 8px; }
.upload-hint kbd {
  display: inline-block;
  padding: 2px 7px;
  font-size: 11px;
  font-family: inherit;
  color: var(--text-secondary);
  background: var(--glass-bg);
  border: 1px solid var(--border-light);
  border-radius: 6px;
}

.preview-area {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.preview-area img {
  display: block;
  width: 100%;
  max-height: 320px;
  object-fit: contain;
  background: rgba(123, 97, 255, 0.04);
}
.preview-overlay {
  position: absolute;
  inset: 0;
  background: rgba(26, 21, 40, 0.55);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  opacity: 0;
  transition: opacity var(--transition);
}
.preview-area:hover .preview-overlay { opacity: 1; }

.overlay-icon {
  width: 44px; height: 44px;
  background: rgba(255,255,255,0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clear-btn {
  position: absolute;
  top: 12px; right: 12px;
  width: 30px; height: 30px;
  border: none;
  background: rgba(26, 21, 40, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 2;
  transition: all var(--transition-fast);
}
.clear-btn:hover {
  background: #E74C3C;
  transform: scale(1.1);
}
</style>
