<template>
  <div class="home-page">
    <!-- Hero -->
    <div class="hero">
      <div class="hero-icon">
        <div class="icon-glow"></div>
        <el-icon :size="48"><PictureFilled /></el-icon>
      </div>
      <h1 class="hero-title">超级图像工具箱</h1>
      <p class="hero-subtitle">
        <span class="highlight">45+</span> 个专业工具，
        <span class="icon-row">
          <el-icon :size="14"><Crop /></el-icon>
          <el-icon :size="14"><Scissor /></el-icon>
          <el-icon :size="14"><MagicStick /></el-icon>
          <el-icon :size="14"><Grid /></el-icon>
        </span>
        一个搜索框找到你想要的
      </p>
    </div>

    <!-- Recent tools -->
    <div v-if="recentTools.length > 0 && !searched && !searching" class="recent-section">
      <div class="recent-row">
        <span
          v-for="t in recentTools"
          :key="t.path"
          class="recent-chip"
          @click="goTo(t.path)"
        >
          <el-icon :size="14"><component :is="t.icon" /></el-icon>
          <span>{{ t.title }}</span>
        </span>
      </div>
    </div>

    <!-- Search -->
    <div class="search-section">
      <div class="search-box">
        <el-icon :size="20" class="search-icon"><Search /></el-icon>
        <input
          v-model="query"
          class="search-input"
          placeholder='描述你想做什么，比如"把背景去掉"、"压缩图片大小"...'
          @input="onInput"
          @keydown.enter="doSearch"
        />
        <el-icon
          v-if="query"
          :size="16"
          class="clear-icon"
          @click="onClear"
        ><Close /></el-icon>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="searching" class="status-text">
      <el-icon class="spin" :size="20"><Loading /></el-icon>
      <span>搜索中...</span>
    </div>

    <!-- Results -->
    <div v-else-if="results.length > 0" class="results-grid">
      <div
        v-for="item in results"
        :key="item.path"
        class="result-card"
        @click="goTo(item.path)"
      >
        <div class="card-top">
          <div class="card-icon-box">
            <el-icon :size="18"><component :is="item.icon" /></el-icon>
          </div>
          <div class="card-info">
            <span class="card-title">{{ item.title }}</span>
            <span class="card-cat">{{ item.category }}</span>
          </div>
          <span class="card-score">{{ Math.round(item.score * 100) }}%</span>
        </div>
      </div>
    </div>

    <!-- No results -->
    <div v-else-if="searched && !searching" class="status-text empty">
      <el-icon :size="40"><Search /></el-icon>
      <p>没有匹配的功能，试试其他描述</p>
    </div>

    <!-- Initial state: Categories -->
    <div v-if="!searched && !searching" class="categories-section">
      <div class="section-head">
        <span class="section-title">按分类浏览</span>
        <span class="section-line"></span>
      </div>
      <div class="pill-grid">
        <button
          v-for="(label, key) in CATEGORY_NAMES"
          :key="key"
          class="pill"
          @click="searchCategory(label)"
        >{{ label }}</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { smartSearch, type SearchResult } from '@/api'
import { CATEGORIES, ROUTES } from '@/router'

const CATEGORY_NAMES = CATEGORIES

const router = useRouter()
const query = ref('')
const results = ref<SearchResult[]>([])
const searching = ref(false)
const searched = ref(false)
const recentTools = ref<{ path: string; title: string; icon: string }[]>([])
let debounceTimer: ReturnType<typeof setTimeout> | null = null

// Load recent tools from localStorage
onMounted(() => {
  try {
    const raw = localStorage.getItem('recent-tools')
    if (raw) {
      const paths: string[] = JSON.parse(raw)
      recentTools.value = paths
        .map(p => ROUTES.find(r => r.path === p))
        .filter(Boolean)
        .slice(0, 4)
        .map(r => ({
          path: r!.path,
          title: (r!.meta as any)?.title ?? '',
          icon: (r!.meta as any)?.icon ?? 'Picture',
        }))
    }
  } catch { /* ignore */ }
})

function saveRecent(path: string) {
  try {
    const raw = localStorage.getItem('recent-tools')
    const paths: string[] = raw ? JSON.parse(raw) : []
    const updated = [path, ...paths.filter(p => p !== path)].slice(0, 4)
    localStorage.setItem('recent-tools', JSON.stringify(updated))
  } catch { /* ignore */ }
}

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
  saveRecent(path)
  router.push(path)
}
</script>

<style scoped>
.home-page {
  max-width: 680px;
  margin: 0 auto;
  padding: 80px 20px 60px;
}

/* ===== Hero ===== */
.hero {
  text-align: center;
  margin-bottom: 40px;
}

.hero-icon {
  position: relative;
  width: 96px;
  height: 96px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  animation: breathe 3s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { box-shadow: 0 0 0 0 rgba(124, 58, 237, 0.4); }
  50% { box-shadow: 0 0 0 18px rgba(124, 58, 237, 0); }
}

.icon-glow {
  position: absolute;
  inset: -6px;
  border-radius: 28px;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(167, 139, 250, 0.1));
  filter: blur(12px);
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.08); }
}

.hero-title {
  font-size: 28px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.5px;
  margin: 0 0 12px;
}

.hero-subtitle {
  font-size: 15px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  flex-wrap: wrap;
  margin: 0;
}

.hero-subtitle .highlight {
  color: var(--primary);
  font-weight: 700;
  font-size: 18px;
}

.icon-row {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  color: var(--primary-light);
  vertical-align: middle;
}

/* ===== Recent Tools ===== */
.recent-section {
  margin-bottom: 28px;
}

.recent-row {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.recent-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition);
}

.recent-chip:hover {
  border-color: var(--primary-light);
  color: var(--primary);
  background: rgba(124, 58, 237, 0.04);
  transform: translateY(-1px);
}

/* ===== Search ===== */
.search-section {
  margin-bottom: 32px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  height: 48px;
  background: #F1F5F9;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 0 16px;
  transition: all 0.25s ease;
}

.search-box:focus-within {
  background: #fff;
  border-color: #7C3AED;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.search-icon {
  color: var(--primary);
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  height: 100%;
  border: none;
  background: transparent;
  outline: none;
  font-size: 15px;
  color: var(--text-primary);
  padding: 0 12px;
  font-family: inherit;
}

.search-input::placeholder {
  color: #999;
  font-size: 14px;
}

.clear-icon {
  color: #bbb;
  cursor: pointer;
  flex-shrink: 0;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.15s;
}

.clear-icon:hover {
  color: #666;
  background: rgba(0,0,0,0.06);
}

/* ===== Status ===== */
.status-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--text-muted);
  padding: 48px 0;
  font-size: 14px;
}

.status-text.empty {
  flex-direction: column;
  gap: 16px;
  font-size: 15px;
}

.status-text.empty p { margin: 0; }

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ===== Results ===== */
.results-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 14px 18px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.result-card:hover {
  border-color: var(--primary-light);
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.1);
  transform: translateY(-1px);
}

.card-top {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon-box {
  width: 36px;
  height: 36px;
  background: rgba(124, 58, 237, 0.08);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  flex-shrink: 0;
}

.card-info {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  display: block;
}

.card-cat {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 1px;
  display: block;
}

.card-score {
  font-size: 13px;
  color: var(--primary);
  font-weight: 700;
  background: rgba(124, 58, 237, 0.08);
  padding: 4px 10px;
  border-radius: 12px;
  flex-shrink: 0;
}

/* ===== Categories ===== */
.categories-section {
  margin-top: 56px;
}

.section-head {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.section-line {
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.pill-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.pill {
  padding: 8px 16px;
  background: #F1F5F9;
  border: none;
  border-radius: 20px;
  font-size: 13px;
  font-family: inherit;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.pill:hover {
  background: var(--primary);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
}

.pill:active {
  transform: scale(0.97);
}
</style>
