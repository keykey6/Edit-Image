<template>
  <div class="home-page">
    <!-- Hero -->
    <div class="hero">
      <div class="hero-icon">
        <el-icon :size="48"><PictureFilled /></el-icon>
      </div>
      <h1 class="hero-title">超级图像工具箱</h1>
      <p class="hero-subtitle">45个工具，一个搜索框找到你想要的</p>
    </div>

    <!-- Search -->
    <div class="search-section">
      <el-input
        v-model="query"
        size="large"
        placeholder='描述你想做什么，比如"把背景去掉"、"压缩图片大小"...'
        clearable
        @input="onInput"
        @clear="onClear"
        @keydown.enter="doSearch"
      >
        <template #prefix>
          <el-icon :size="20"><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- Loading -->
    <div v-if="searching" class="status-text">搜索中...</div>

    <!-- Results -->
    <div v-else-if="results.length > 0" class="results-grid">
      <div
        v-for="item in results"
        :key="item.path"
        class="result-card"
        @click="goTo(item.path)"
      >
        <div class="card-top">
          <el-icon :size="22"><component :is="item.icon" /></el-icon>
          <span class="card-title">{{ item.title }}</span>
          <span class="card-score">{{ Math.round(item.score * 100) }}%</span>
        </div>
        <p class="card-desc">{{ item.description }}</p>
        <el-tag size="small" type="info">{{ item.category }}</el-tag>
      </div>
    </div>

    <!-- No results -->
    <div v-else-if="searched && !searching" class="status-text empty">
      <el-icon :size="36"><Search /></el-icon>
      <p>没有匹配的功能，试试其他描述</p>
    </div>

    <!-- Initial state: Categories -->
    <div v-if="!searched && !searching" class="categories-section">
      <h3 class="section-title">按分类浏览</h3>
      <div class="category-tags">
        <span
          v-for="(label, key) in CATEGORY_NAMES"
          :key="key"
          class="category-tag"
          @click="searchCategory(label)"
        >{{ label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { smartSearch, type SearchResult } from '@/api'
import { CATEGORIES } from '@/router'

// 图标已全局注册（见 main.ts），直接使用 component :is="item.icon"

const CATEGORY_NAMES = CATEGORIES

const router = useRouter()
const query = ref('')
const results = ref<SearchResult[]>([])
const searching = ref(false)
const searched = ref(false)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

function onInput() {
  searched.value = false
  if (debounceTimer) clearTimeout(debounceTimer)
  if (!query.value.trim()) {
    onClear()
    return
  }
  debounceTimer = setTimeout(doSearch, 300)
}

function onClear() {
  if (debounceTimer) clearTimeout(debounceTimer)
  query.value = ''
  results.value = []
  searching.value = false
  searched.value = false
}

async function doSearch() {
  const q = query.value.trim()
  if (!q) return

  searching.value = true
  searched.value = true
  results.value = []

  try {
    const res = await smartSearch(q, 5)
    results.value = res.results
  } catch {
    results.value = []
  } finally {
    searching.value = false
  }
}

function searchCategory(label: string) {
  query.value = label
  doSearch()
}

function goTo(path: string) {
  router.push(path)
}
</script>

<style scoped>
.home-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 60px 20px;
}

/* Hero */
.hero { text-align: center; margin-bottom: 32px; }
.hero-icon {
  width: 80px; height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #6C5CE7, #a29bfe);
  border-radius: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.hero-title { font-size: 28px; font-weight: 800; color: var(--text-primary); margin: 0 0 8px; }
.hero-subtitle { font-size: 15px; color: var(--text-muted); margin: 0; }

/* Search */
.search-section { margin-bottom: 28px; }
.search-section :deep(.el-input__wrapper) {
  border-radius: 14px;
  padding: 6px 16px;
  box-shadow: 0 2px 12px rgba(108, 92, 231, 0.1);
}

/* Status */
.status-text { text-align: center; color: var(--text-muted); padding: 40px 0; }
.status-text.empty { color: var(--text-muted); }
.status-text.empty p { margin-top: 12px; }

/* Results */
.results-grid { display: flex; flex-direction: column; gap: 10px; }
.result-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px 20px;
  cursor: pointer;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.result-card:hover {
  border-color: var(--primary-light);
  box-shadow: 0 4px 16px rgba(108, 92, 231, 0.12);
}
.card-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}
.card-title { font-size: 15px; font-weight: 600; color: var(--text-primary); }
.card-score {
  margin-left: auto;
  font-size: 12px;
  color: var(--primary);
  font-weight: 600;
}
.card-desc { font-size: 13px; color: var(--text-secondary); margin: 0 0 8px; }

/* Categories */
.categories-section { margin-top: 48px; }
.section-title { font-size: 14px; color: var(--text-muted); margin: 0 0 14px; text-align: center; }
.category-tags { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
.category-tag {
  padding: 8px 20px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 22px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}
.category-tag:hover {
  border-color: var(--primary-light);
  color: var(--primary);
  background: rgba(108, 92, 231, 0.04);
}
</style>
