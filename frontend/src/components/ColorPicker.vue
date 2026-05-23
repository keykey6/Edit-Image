<template>
  <div class="color-picker">
    <label>{{ label }}</label>
    <div class="color-options">
      <button
        v-for="c in colors"
        :key="c.value"
        :class="{ active: modelValue === c.value }"
        :style="{ background: c.value }"
        @click="$emit('update:modelValue', c.value)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  modelValue: string
  colors: { value: string; label: string }[]
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<style scoped>
.color-picker {
  padding: 4px 0;
}
.color-picker > label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}
.color-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.color-options button {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform var(--transition), border-color var(--transition);
}
.color-options button:hover {
  transform: scale(1.15);
}
.color-options button.active {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.2);
}
</style>
