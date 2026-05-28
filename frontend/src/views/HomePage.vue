<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-dot" />
          <span>45+ 图像处理工具 · 完全本地运行</span>
        </div>

        <h1 class="hero-title">
          让 UI 设计<span class="text-gradient">更简单</span>，<br />
          让开发<span class="text-gradient">更专注</span>
        </h1>

        <p class="hero-subtitle">
          聚焦素材切割和 Design.md 生成，设计素材管理、规范沉淀与排版工具<br />
          扩展创意同一个工作台。
        </p>

        <div class="hero-tags">
          <span class="tag"><el-icon :size="13"><Collection /></el-icon>素材切割</span>
          <span class="tag"><el-icon :size="13"><Document /></el-icon>开发设计</span>
          <span class="tag"><el-icon :size="13"><MagicStick /></el-icon>高效管理</span>
          <span class="tag"><el-icon :size="13"><Refresh /></el-icon>持续更新</span>
        </div>
      </div>

      <!-- Hero Visual -->
      <div class="hero-visual">
        <div class="glass-card card-main">
          <div class="card-icon-lg">
            <el-icon :size="28"><UploadFilled /></el-icon>
          </div>
        </div>
        <div class="glass-card card-float card-1">
          <div class="mini-icon"><el-icon :size="16"><Crop /></el-icon></div>
          <span class="mini-label">素材切割</span>
        </div>
        <div class="glass-card card-float card-2">
          <div class="mini-icon purple"><el-icon :size="16"><EditPen /></el-icon></div>
          <span class="mini-label">Design.md</span>
        </div>
        <div class="glass-card card-float card-3">
          <div class="mini-icon"><el-icon :size="16"><Grid /></el-icon></div>
          <span class="mini-label">更多工具</span>
        </div>
      </div>
    </section>

    <!-- Search Section -->
    <section class="search-section">
      <div class="search-glass">
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
    </section>

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

    <!-- Loading -->
    <div v-if="searching" class="status-text">
      <div class="spinner" />
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

    <!-- Tools Grid Section -->
    <section v-if="!searched && !searching" id="tools-section" class="tools-section">
      <div class="section-header">
        <h2 class="section-title">常用工具</h2>
        <p class="section-desc">借助 AI 工具箱释放上线创意无限潜力，高效素材处理与设计规范生成</p>
      </div>

      <div class="tools-grid">
        <div
          v-for="tool in featuredTools"
          :key="tool.path"
          class="tool-card"
          @click="goTo(tool.path)"
        >
          <div class="tool-card-header">
            <div class="tool-icon-wrap" :class="tool.color">
              <el-icon :size="20"><component :is="tool.icon" /></el-icon>
            </div>
            <div class="tool-meta">
              <span class="tool-name">{{ tool.title }}</span>
              <span class="tool-cat">{{ tool.category }}</span>
            </div>
            <el-icon :size="14" class="tool-arrow"><ArrowRight /></el-icon>
          </div>
          <div class="tool-tags">
            <span v-for="tag in tool.tags" :key="tag" class="tool-tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section v-if="!searched && !searching" class="categories-section">
      <div class="section-header">
        <h2 class="section-title">按分类浏览</h2>
      </div>
      <div class="pill-grid">
        <button
          v-for="(label, key) in CATEGORY_NAMES"
          :key="key"
          class="pill"
          @click="searchCategory(label)"
        >{{ label }}</button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="home-footer">
      <div class="footer-brand">
        <div class="footer-icon">
          <el-icon :size="16"><PictureFilled /></el-icon>
        </div>
        <span class="footer-text">VibeUI Kit</span>
      </div>
    </footer>
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

// Featured tools for the grid
const featuredTools = [
  { path: '/grid-split', title: '素材切割', category: '拼接与布局', icon: 'Operation', color: 'purple', tags: ['智能切割', '网格裁剪', '批量'] },
  { path: '/color-filter', title: 'Design.md', category: '颜色与光影', icon: 'MagicStick', color: 'blue', tags: ['Design Tokens', 'Harmony', '色彩规范'] },
  { path: '/batch-process', title: '更多工具', category: '批量操作', icon: 'Grid', color: 'pink', tags: ['批量上传', '模板管理', '持续更新'] },
]

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
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 24px 60px;
}

/* ===== Hero ===== */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 48px;
  margin-bottom: 48px;
  padding-top: 20px;
}

.hero-content {
  flex: 1;
  min-width: 0;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.badge-dot {
  width: 6px; height: 6px;
  background: linear-gradient(135deg, #7B61FF, #A78BFA);
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.15); }
}

.hero-title {
  font-family: 'Outfit', sans-serif;
  font-size: 42px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.2;
  letter-spacing: -1px;
  margin: 0 0 16px;
}

.text-gradient {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, #C4B5FD 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 15px;
  color: var(--text-muted);
  line-height: 1.7;
  margin: 0 0 24px;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

/* ===== Hero Visual ===== */
.hero-visual {
  position: relative;
  width: 320px;
  height: 280px;
  flex-shrink: 0;
}

.glass-card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.card-main {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 120px; height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float-main 6s ease-in-out infinite;
}

.card-icon-lg {
  width: 56px; height: 56px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 8px 24px rgba(123, 97, 255, 0.35);
}

.card-float {
  position: absolute;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: float 5s ease-in-out infinite;
}

.card-1 { top: 20px; left: 0; animation-delay: 0s; }
.card-2 { top: 0; right: 10px; animation-delay: 1.5s; }
.card-3 { bottom: 30px; right: 0; animation-delay: 3s; }

.mini-icon {
  width: 32px; height: 32px;
  background: rgba(123, 97, 255, 0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}
.mini-icon.purple {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: #fff;
}

.mini-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
@keyframes float-main {
  0%, 100% { transform: translate(-50%, -50%) translateY(0); }
  50% { transform: translate(-50%, -50%) translateY(-5px); }
}

/* ===== Search ===== */
.search-section {
  margin-bottom: 24px;
}

.search-glass {
  position: relative;
  display: flex;
  align-items: center;
  height: 52px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: 0 20px;
  box-shadow: var(--shadow);
  transition: all var(--transition);
}
.search-glass:focus-within {
  border-color: rgba(123, 97, 255, 0.4);
  box-shadow: 0 0 0 4px rgba(123, 97, 255, 0.08), var(--shadow-md);
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
  padding: 0 14px;
  font-family: inherit;
}
.search-input::placeholder {
  color: var(--text-placeholder);
  font-size: 14px;
}

.clear-icon {
  color: var(--text-muted);
  cursor: pointer;
  flex-shrink: 0;
  padding: 4px;
  border-radius: 50%;
  transition: all var(--transition-fast);
}
.clear-icon:hover {
  color: var(--text-secondary);
  background: rgba(0,0,0,0.04);
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
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-full);
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition);
}
.recent-chip:hover {
  border-color: rgba(123, 97, 255, 0.3);
  color: var(--primary);
  background: rgba(123, 97, 255, 0.06);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

/* ===== Status ===== */
.status-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
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

.spinner {
  width: 20px; height: 20px;
  border: 2px solid var(--border-color);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ===== Results ===== */
.results-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 40px;
}

.result-card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  padding: 14px 18px;
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: var(--shadow-sm);
}
.result-card:hover {
  border-color: rgba(123, 97, 255, 0.3);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-top {
  display: flex;
  align-items: center;
  gap: 12px;
}

.card-icon-box {
  width: 38px; height: 38px;
  background: rgba(123, 97, 255, 0.1);
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
  margin-top: 2px;
  display: block;
}

.card-score {
  font-size: 12px;
  color: var(--primary);
  font-weight: 700;
  background: rgba(123, 97, 255, 0.1);
  padding: 4px 10px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

/* ===== Tools Section ===== */
.tools-section {
  margin-top: 56px;
}

.section-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-title {
  font-family: 'Outfit', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px;
  letter-spacing: -0.3px;
}

.section-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin-bottom: 48px;
}

.tool-card {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: var(--shadow-sm);
}
.tool-card:hover {
  border-color: rgba(123, 97, 255, 0.3);
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

.tool-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.tool-icon-wrap {
  width: 40px; height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.tool-icon-wrap.purple {
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  color: #fff;
  box-shadow: 0 4px 14px rgba(123, 97, 255, 0.3);
}
.tool-icon-wrap.blue {
  background: linear-gradient(135deg, #60A5FA, #93C5FD);
  color: #fff;
  box-shadow: 0 4px 14px rgba(96, 165, 250, 0.3);
}
.tool-icon-wrap.pink {
  background: linear-gradient(135deg, #F472B6, #F9A8D4);
  color: #fff;
  box-shadow: 0 4px 14px rgba(244, 114, 182, 0.3);
}

.tool-meta {
  flex: 1;
  min-width: 0;
}

.tool-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  display: block;
}

.tool-cat {
  font-size: 12px;
  color: var(--text-muted);
  display: block;
  margin-top: 2px;
}

.tool-arrow {
  color: var(--text-muted);
  transition: all var(--transition-fast);
}
.tool-card:hover .tool-arrow {
  color: var(--primary);
  transform: translateX(3px);
}

.tool-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tool-tag {
  padding: 4px 10px;
  background: rgba(123, 97, 255, 0.06);
  border-radius: var(--radius-full);
  font-size: 11px;
  color: var(--text-muted);
}

/* ===== Categories ===== */
.categories-section {
  margin-top: 48px;
}

.pill-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.pill {
  padding: 9px 18px;
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
.pill:hover {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(123, 97, 255, 0.35);
}
.pill:active {
  transform: scale(0.97);
}

/* ===== Footer ===== */
.home-footer {
  margin-top: 64px;
  padding-top: 32px;
  border-top: 1px solid var(--divider);
  display: flex;
  justify-content: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0.5;
}

.footer-icon {
  width: 28px; height: 28px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.footer-text {
  font-family: 'Outfit', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
}

/* 响应式 */
@media (max-width: 768px) {
  .home-page { padding: 24px 16px 40px; }
  .hero {
    flex-direction: column;
    text-align: center;
    gap: 32px;
  }
  .hero-visual {
    width: 100%;
    height: 200px;
  }
  .hero-title {
    font-size: 28px;
    letter-spacing: -0.5px;
  }
  .hero-subtitle {
    font-size: 14px;
  }
  .tools-grid {
    grid-template-columns: 1fr;
  }
  .card-main {
    width: 90px; height: 90px;
  }
  .card-float {
    padding: 8px 12px;
  }
  .card-1 { top: 10px; left: 10px; }
  .card-2 { top: 0; right: 20px; }
  .card-3 { bottom: 20px; right: 10px; }
}

@media (max-width: 480px) {
  .hero-title { font-size: 24px; }
  .hero-tags { justify-content: center; }
  .tag { font-size: 11px; padding: 6px 10px; }
}
</style>
