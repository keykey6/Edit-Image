<template>
  <div class="compare-wrap">
    <div class="compare-tabs">
      <button :class="{ active: mode === 'side' }" @click="mode = 'side'">
        <el-icon :size="16"><Grid /></el-icon> 并排
      </button>
      <button :class="{ active: mode === 'slider' }" @click="mode = 'slider'">
        <el-icon :size="16"><Switch /></el-icon> 滑动
      </button>
    </div>

    <!-- Side-by-side -->
    <div v-if="mode === 'side'" class="compare-side">
      <div class="compare-pane">
        <div class="pane-label">原图</div>
        <img v-if="original" :src="original" alt="原图" />
        <div v-else class="pane-empty">暂无原图</div>
      </div>
      <div class="compare-pane">
        <div class="pane-label">处理后</div>
        <img v-if="processed" :src="processed" alt="处理后" />
        <div v-else class="pane-empty">暂无结果</div>
      </div>
    </div>

    <!-- Slider -->
    <div v-else class="compare-slider" ref="sliderRef" @mousedown="startDrag" @touchstart.prevent="startDrag">
      <div class="slider-before">
        <img v-if="original" :src="original" alt="原图" />
      </div>
      <div class="slider-after" :style="{ clipPath: `inset(0 0 0 ${pos}%)` }">
        <img v-if="processed" :src="processed" alt="处理后" />
      </div>
      <div class="slider-handle" :style="{ left: pos + '%' }">
        <div class="handle-line" />
        <div class="handle-knob">
          <el-icon :size="14"><ArrowLeft /></el-icon>
          <el-icon :size="14"><ArrowRight /></el-icon>
        </div>
      </div>
      <div class="slider-label left">原图</div>
      <div class="slider-label right">处理后</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ original?: string; processed?: string }>()

const mode = ref<'side' | 'slider'>('slider')
const pos = ref(50)
const sliderRef = ref<HTMLDivElement>()

function startDrag(e: MouseEvent | TouchEvent) {
  const el = sliderRef.value
  if (!el) return
  const rect = el.getBoundingClientRect()

  function onMove(ev: MouseEvent | TouchEvent) {
    const clientX = 'touches' in ev ? ev.touches[0].clientX : ev.clientX
    const pct = ((clientX - rect.left) / rect.width) * 100
    pos.value = Math.max(2, Math.min(98, pct))
  }

  function onUp() {
    document.removeEventListener('mousemove', onMove)
    document.removeEventListener('mouseup', onUp)
    document.removeEventListener('touchmove', onMove)
    document.removeEventListener('touchend', onUp)
  }

  document.addEventListener('mousemove', onMove)
  document.addEventListener('mouseup', onUp)
  document.addEventListener('touchmove', onMove, { passive: false })
  document.addEventListener('touchend', onUp)
}
</script>

<style scoped>
.compare-wrap {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.compare-tabs {
  display: flex;
  gap: 4px;
  padding: 10px 16px;
  border-bottom: 1px solid var(--border-color);
  background: var(--content-bg);
}
.compare-tabs button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  border: none;
  border-radius: 20px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}
.compare-tabs button.active {
  background: var(--primary);
  color: #fff;
}

/* Side-by-side */
.compare-side { display: flex; gap: 2px; background: var(--border-color); }
.compare-pane {
  flex: 1;
  min-height: 280px;
  background: var(--card-bg);
  position: relative;
}
.compare-pane img { width: 100%; height: 300px; object-fit: contain; display: block; }
.pane-empty {
  display: flex; align-items: center; justify-content: center;
  height: 300px; color: var(--text-muted); font-size: 14px;
}
.pane-label {
  position: absolute; top: 10px; left: 14px;
  padding: 3px 10px; border-radius: 12px;
  background: rgba(0,0,0,0.55); color: #fff;
  font-size: 12px; z-index: 1;
}

/* Slider */
.compare-slider {
  position: relative;
  width: 100%; height: 400px;
  overflow: hidden;
  user-select: none;
  cursor: ew-resize;
  background: #e2e8f0;
}
.slider-before, .slider-after {
  position: absolute; inset: 0;
}
.slider-before img, .slider-after img {
  width: 100%; height: 100%; object-fit: contain;
}
.slider-after { z-index: 1; }

.slider-handle {
  position: absolute; top: 0; bottom: 0;
  width: 4px; margin-left: -2px;
  z-index: 2;
}
.handle-line {
  width: 100%; height: 100%;
  background: #fff;
  box-shadow: 0 0 8px rgba(0,0,0,0.3);
}
.handle-knob {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 36px; height: 36px;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 2px 12px rgba(0,0,0,0.2);
  display: flex; align-items: center; justify-content: center;
  gap: 0px; color: var(--primary);
}

.slider-label {
  position: absolute; top: 14px;
  padding: 3px 10px; border-radius: 12px;
  background: rgba(0,0,0,0.5); color: #fff;
  font-size: 12px; z-index: 3;
}
.slider-label.left { left: 14px; }
.slider-label.right { right: 14px; }
</style>
