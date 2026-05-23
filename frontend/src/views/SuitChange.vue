<template>
  <ToolPage module="suit-change" :params="params">
    <template #params>
      <label class="param-label">正装颜色</label>
      <div class="color-options">
        <button
          v-for="c in colors"
          :key="c.value"
          :class="{ active: params.color === c.value }"
          :style="{ background: c.hex }"
          @click="params.color = c.value"
        />
        <span class="color-name">{{ colors.find(c => c.value === params.color)?.label }}</span>
      </div>
    </template>
  </ToolPage>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import ToolPage from '@/components/ToolPage.vue'

const params = reactive<Record<string, unknown>>({
  color: 'black',
})

const colors = [
  { value: 'black', label: '黑色', hex: '#28282d' },
  { value: 'navy', label: '藏青', hex: '#1e2850' },
  { value: 'gray', label: '灰色', hex: '#64646e' },
  { value: 'white', label: '白色', hex: '#dcdce1' },
]
</script>

<style scoped>
.param-label {
  display: block;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}
.color-options {
  display: flex;
  gap: 12px;
  align-items: center;
}
.color-options button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 3px solid transparent;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
}
.color-options button:hover {
  transform: scale(1.15);
}
.color-options button.active {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(108, 92, 231, 0.2);
}
.color-name {
  font-size: 14px;
  color: var(--text-primary);
  margin-left: 4px;
}
</style>
