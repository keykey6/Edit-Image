<template>
  <div class="empty-state">
    <div class="empty-icon">
      <el-icon :size="64"><Picture /></el-icon>
    </div>
    <h3 class="empty-title">{{ title }}</h3>
    <p class="empty-desc">上传图片开始体验，所有处理均在本地完成</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title: string }>()
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
}
.empty-icon {
  color: var(--primary-light);
  margin-bottom: 20px;
  opacity: 0.6;
}
.empty-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}
.empty-desc {
  font-size: 14px;
  color: var(--text-secondary);
}
</style>
