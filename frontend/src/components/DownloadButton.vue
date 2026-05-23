<template>
  <button class="download-btn" :disabled="disabled">
    <el-icon :size="18"><Download /></el-icon>
    {{ label }}
  </button>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  label?: string
  disabled?: boolean
}>(), {
  label: '一键下载',
  disabled: false,
})
</script>

<style scoped>
.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary), #a29bfe);
  color: #fff;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
}
.download-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(108, 92, 231, 0.35);
}
.download-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
