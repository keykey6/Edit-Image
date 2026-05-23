<template>
  <div class="param-slider">
    <div class="param-header">
      <label>{{ label }}</label>
      <span class="param-value">{{ modelValue }}{{ unit }}</span>
    </div>
    <el-slider
      :model-value="modelValue"
      :min="min"
      :max="max"
      :step="step"
      :show-tooltip="false"
      @update:model-value="$emit('update:modelValue', $event)"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  modelValue: number
  min?: number
  max?: number
  step?: number
  unit?: string
}>()

defineEmits<{
  'update:modelValue': [value: number]
}>()
</script>

<style scoped>
.param-slider {
  padding: 4px 0;
}
.param-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}
.param-header label {
  font-size: 13px;
  color: var(--text-secondary);
}
.param-value {
  font-size: 13px;
  color: var(--primary);
  font-weight: 500;
}
</style>
