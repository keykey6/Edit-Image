<template>
  <div class="all-tools-page">
    <!-- Page Header -->
    <div class="page-hero">
      <h1 class="page-hero-title">全部工具</h1>
      <p class="page-hero-desc">45+ 个专业图像处理工具，覆盖设计工作流的每个环节</p>

      <!-- Category Filter -->
      <div class="filter-bar">
        <button
          class="filter-pill"
          :class="{ active: activeCat === '' }"
          @click="activeCat = ''"
        >全部</button>
        <button
          v-for="(label, key) in CATEGORIES"
          :key="key"
          class="filter-pill"
          :class="{ active: activeCat === key }"
          @click="activeCat = key"
        >{{ label }}</button>
      </div>
    </div>

    <!-- Tools by Category -->
    <div class="tools-container">
      <div
        v-for="cat in filteredCategories"
        :key="cat.key"
        class="cat-section"
        :id="'cat-' + cat.key"
      >
        <div class="cat-header">
          <div class="cat-icon-wrap">
            <el-icon :size="20"><component :is="cat.icon" /></el-icon>
          </div>
          <div class="cat-meta">
            <h2 class="cat-title">{{ cat.label }}</h2>
            <p class="cat-desc">{{ DESCRIPTIONS[cat.key] }}</p>
          </div>
          <span class="cat-count">{{ cat.items.length }} 个工具</span>
        </div>

        <div class="cat-grid">
          <router-link
            v-for="item in cat.items"
            :key="item.path"
            :to="item.path"
            class="tool-item"
          >
            <div class="tool-item-icon">
              <el-icon :size="22"><component :is="item.icon" /></el-icon>
            </div>
            <div class="tool-item-info">
              <span class="tool-item-name">{{ item.title }}</span>
              <span class="tool-item-arrow"><el-icon :size="14"><ArrowRight /></el-icon></span>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredCategories.length === 0" class="empty-state">
      <el-icon :size="48"><Search /></el-icon>
      <p>没有找到匹配的工具</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ROUTES, CATEGORIES, DESCRIPTIONS } from '@/router'

const activeCat = ref('')

const categoryIcons: Record<string, string> = {
  basic: 'Picture',
  color: 'MagicStick',
  effects: 'Brush',
  portrait: 'Camera',
  privacy: 'Lock',
  layout: 'Grid',
  convert: 'Switch',
  generate: 'Postcard',
  analysis: 'DataAnalysis',
  batch: 'List',
}

const categories = computed(() => {
  const map = new Map<string, { path: string; title: string; icon: string }[]>()
  for (const r of ROUTES) {
    const cat = (r.meta as any)?.category ?? 'basic'
    if (!map.has(cat)) map.set(cat, [])
    map.get(cat)!.push({
      path: r.path,
      title: (r.meta as any)?.title ?? '',
      icon: (r.meta as any)?.icon ?? 'Picture',
    })
  }
  return Array.from(map.entries()).map(([key, items]) => ({
    key,
    label: CATEGORIES[key] ?? key,
    desc: DESCRIPTIONS[key] ?? '',
    icon: categoryIcons[key] ?? 'Picture',
    items,
  }))
})

const filteredCategories = computed(() => {
  if (!activeCat.value) return categories.value
  return categories.value.filter(c => c.key === activeCat.value)
})
</script>

<style scoped>
.all-tools-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 24px 60px;
}

/* ===== Page Hero ===== */
.page-hero {
  text-align: center;
  margin-bottom: 40px;
}

.page-hero-title {
  font-family: 'Outfit', sans-serif;
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.5px;
  margin: 0 0 8px;
}

.page-hero-desc {
  font-size: 15px;
  color: var(--text-muted);
  margin: 0 0 24px;
}

/* ===== Filter Bar ===== */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.filter-pill {
  padding: 8px 18px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
  font-size: 13px;
  font-family: inherit;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition);
  font-weight: 500;
  box-shadow: var(--shadow-sm);
}
.filter-pill:hover {
  border-color: rgba(123, 97, 255, 0.3);
  transform: translateY(-1px);
}
.filter-pill.active {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  border-color: transparent;
  box-shadow: 0 4px 16px rgba(123, 97, 255, 0.35);
}

/* ===== Category Section ===== */
.tools-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.cat-section {
  animation: fade-up 0.4s ease both;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.cat-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--divider);
}

.cat-icon-wrap {
  width: 42px; height: 42px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(123, 97, 255, 0.3);
}

.cat-meta {
  flex: 1;
  min-width: 0;
}

.cat-title {
  font-family: 'Outfit', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.2px;
}

.cat-desc {
  font-size: 12px;
  color: var(--text-muted);
  margin: 2px 0 0;
}

.cat-count {
  font-size: 12px;
  color: var(--primary);
  font-weight: 600;
  background: rgba(123, 97, 255, 0.08);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

/* ===== Tool Grid ===== */
.cat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.tool-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  text-decoration: none;
  transition: all var(--transition);
  box-shadow: var(--shadow-sm);
}
.tool-item:hover {
  border-color: rgba(123, 97, 255, 0.3);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.tool-item-icon {
  width: 36px; height: 36px;
  background: rgba(123, 97, 255, 0.08);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  flex-shrink: 0;
  transition: all var(--transition-fast);
}
.tool-item:hover .tool-item-icon {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: #fff;
  box-shadow: 0 4px 12px rgba(123, 97, 255, 0.3);
}

.tool-item-info {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-width: 0;
}

.tool-item-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.tool-item-arrow {
  color: var(--text-muted);
  transition: all var(--transition-fast);
}
.tool-item:hover .tool-item-arrow {
  color: var(--primary);
  transform: translateX(3px);
}

/* ===== Empty State ===== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 60px 0;
  color: var(--text-muted);
}
.empty-state p {
  font-size: 15px;
  margin: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .all-tools-page { padding: 24px 16px 40px; }
  .page-hero-title { font-size: 26px; }
  .cat-grid { grid-template-columns: repeat(2, 1fr); }
  .cat-header { flex-wrap: wrap; }
  .cat-count { margin-left: auto; }
}

@media (max-width: 480px) {
  .cat-grid { grid-template-columns: 1fr; }
  .filter-bar { gap: 6px; }
  .filter-pill { padding: 6px 12px; font-size: 12px; }
}
</style>
