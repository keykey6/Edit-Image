<template>
  <div class="layout">
    <!-- 背景装饰光球 -->
    <div class="bg-orb orb-1" />
    <div class="bg-orb orb-2" />
    <div class="bg-orb orb-3" />

    <!-- 顶部导航 -->
    <header class="top-nav" :class="{ 'nav-scrolled': scrolled }">
      <div class="nav-inner">
        <router-link to="/" class="nav-logo">
          <div class="logo-bloom">
            <div class="logo-icon">
              <el-icon :size="18"><PictureFilled /></el-icon>
            </div>
          </div>
          <span class="logo-text">VibeUI Kit</span>
        </router-link>

        <nav class="nav-links">
          <router-link to="/" class="nav-link" exact-active-class="nav-link-active">首页</router-link>
          <router-link to="/all-tools" class="nav-link" exact-active-class="nav-link-active">全部工具</router-link>
          <a class="nav-link" href="#" @click.prevent="showDesignMd = true">Design.md</a>
          <a class="nav-link" href="#" @click.prevent="showSites = true">网站推荐</a>
        </nav>

        <div class="nav-actions">
          <button class="btn-glass btn-sm">立即体验</button>
        </div>
      </div>
    </header>

    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed }">
      <div class="sidebar-glass">
        <!-- Logo -->
        <router-link to="/" class="sidebar-logo">
          <div class="logo-icon-sm">
            <el-icon :size="18"><PictureFilled /></el-icon>
          </div>
          <span class="logo-text-sm">工具箱</span>
        </router-link>

        <!-- Nav -->
        <nav class="sidebar-nav">
          <router-link to="/" class="nav-item" active-class="nav-active" exact-active-class="nav-active">
            <div class="nav-icon-wrap">
              <el-icon :size="18"><HomeFilled /></el-icon>
            </div>
            <span>首页</span>
          </router-link>

          <div class="nav-divider" />

          <div v-for="cat in categories" :key="cat.key" class="nav-group">
            <button class="group-label" @click="toggleCat(cat.key)">
              <span>{{ cat.label }}</span>
              <el-icon class="group-arrow" :class="{ expanded: openCats.has(cat.key) }" :size="12">
                <ArrowDown />
              </el-icon>
            </button>
            <div class="group-items" :class="{ collapsed: !openCats.has(cat.key) }">
              <router-link
                v-for="item in cat.items"
                :key="item.path"
                :to="item.path"
                class="nav-item nav-sub"
                active-class="nav-active"
              >
                <div class="nav-icon-wrap">
                  <el-icon :size="16"><component :is="item.icon" /></el-icon>
                </div>
                <span>{{ item.title }}</span>
              </router-link>
            </div>
          </div>
        </nav>

        <!-- Footer -->
        <div class="sidebar-footer">
          <button class="collapse-btn" @click="collapsed = !collapsed">
            <el-icon :size="14">
              <DArrowLeft v-if="!collapsed" />
              <DArrowRight v-else />
            </el-icon>
            <span>{{ collapsed ? '展开' : '收起' }}</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- Design.md 弹窗 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showDesignMd" class="modal-overlay" @click.self="showDesignMd = false">
          <div class="modal-glass">
            <div class="modal-header">
              <h3 class="modal-title">Design.md</h3>
              <button class="modal-close" @click="showDesignMd = false">
                <el-icon :size="18"><Close /></el-icon>
              </button>
            </div>
            <div class="modal-body">
              <p class="modal-desc">设计规范文档生成工具，帮助你从设计稿中提取 Design Tokens 并生成标准化的 Design.md 文档。</p>
              <div class="modal-features">
                <div class="feature-item">
                  <div class="feature-icon"><el-icon :size="18"><Brush /></el-icon></div>
                  <div class="feature-text">
                    <strong>色彩规范</strong>
                    <span>自动提取主色、辅助色、中性色</span>
                  </div>
                </div>
                <div class="feature-item">
                  <div class="feature-icon"><el-icon :size="18"><Document /></el-icon></div>
                  <div class="feature-text">
                    <strong>字体系统</strong>
                    <span>生成字体层级与行高规范</span>
                  </div>
                </div>
                <div class="feature-item">
                  <div class="feature-icon"><el-icon :size="18"><Grid /></el-icon></div>
                  <div class="feature-text">
                    <strong>间距体系</strong>
                    <span>8px 基准网格与组件间距</span>
                  </div>
                </div>
              </div>
              <div class="modal-action">
                <button class="btn-primary" @click="showDesignMd = false; $router.push('/color-filter')">
                  <el-icon :size="16"><MagicStick /></el-icon>
                  前往调色滤镜工具
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- 网站推荐弹窗 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showSites" class="modal-overlay" @click.self="showSites = false">
          <div class="modal-glass modal-wide">
            <div class="modal-header">
              <h3 class="modal-title">网站推荐</h3>
              <button class="modal-close" @click="showSites = false">
                <el-icon :size="18"><Close /></el-icon>
              </button>
            </div>
            <div class="modal-body">
              <p class="modal-desc">精选设计与开发资源网站，助力你的创意工作流。点击卡片即可复制链接。</p>
              <div class="site-grid">
                <div
                  v-for="site in recommendedSites"
                  :key="site.name"
                  class="site-card"
                  @click="copyLink(site.url)"
                >
                  <div class="site-icon" :style="{ background: site.color }">{{ site.abbr }}</div>
                  <div class="site-info">
                    <strong>{{ site.name }}</strong>
                    <span>{{ site.desc }}</span>
                  </div>
                  <el-icon :size="14" class="site-copy"><CopyDocument /></el-icon>
                </div>
              </div>
              <p v-if="copyTip" class="copy-tip">{{ copyTip }}</p>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- 主内容区 -->
    <main class="content">
      <header v-if="!isHome" class="content-header">
        <div class="header-glass">
          <h1 class="page-title">{{ currentTitle }}</h1>
          <p class="page-desc">{{ currentDesc }}</p>
        </div>
      </header>
      <div class="content-body" :class="{ home: isHome }">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { ROUTES, CATEGORIES, DESCRIPTIONS } from '@/router'

const route = useRoute()

const collapsed = ref(false)
const openCats = reactive(new Set<string>())
const scrolled = ref(false)
const showDesignMd = ref(false)
const showSites = ref(false)

function toggleCat(key: string) {
  if (openCats.has(key)) { openCats.delete(key) } else { openCats.add(key) }
}

function onScroll() {
  scrolled.value = window.scrollY > 20
}

function scrollToTools() {
  if (route.path !== '/') {
    window.location.href = '/#tools-section'
    return
  }
  const el = document.getElementById('tools-section')
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
})
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

const isHome = computed(() => route.path === '/')

const recommendedSites = [
  { name: 'Dribbble', url: 'https://dribbble.com', color: '#EA4C89', abbr: 'Dr', desc: '设计师作品分享平台' },
  { name: 'Figma', url: 'https://www.figma.com', color: '#F24E1E', abbr: 'Fg', desc: '协作式界面设计工具' },
  { name: 'Unsplash', url: 'https://unsplash.com', color: '#000000', abbr: 'Un', desc: '高质量免费图片素材' },
  { name: 'Color Hunt', url: 'https://colorhunt.co', color: 'linear-gradient(135deg, #FF6B6B, #4ECDC4)', abbr: 'Ch', desc: '配色方案灵感库' },
  { name: 'Uiverse', url: 'https://uiverse.io', color: '#6366F1', abbr: 'Ui', desc: '开源 UI 组件库' },
  { name: 'Remove.bg', url: 'https://www.remove.bg', color: '#5C24FC', abbr: 'Rb', desc: 'AI 自动抠图工具' },
]

const copyTip = ref('')
let copyTimer: ReturnType<typeof setTimeout> | null = null

async function copyLink(url: string) {
  try {
    await navigator.clipboard.writeText(url)
    copyTip.value = '链接已复制到剪贴板！'
  } catch {
    copyTip.value = '复制失败，请手动复制'
  }
  if (copyTimer) clearTimeout(copyTimer)
  copyTimer = setTimeout(() => { copyTip.value = '' }, 2000)
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
    items,
  }))
})

const currentTitle = computed(() => {
  const match = ROUTES.find(r => r.path === route.path)
  return match?.meta?.title ?? '首页'
})

const currentDesc = computed(() => {
  const match = ROUTES.find(r => r.path === route.path)
  return DESCRIPTIONS[(match?.meta as any)?.category] ?? ''
})
</script>

<style scoped>
/* ============================
   Layout
   ============================ */
.layout {
  display: flex;
  min-height: 100vh;
  position: relative;
}

/* 背景光球 */
.orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(155, 135, 253, 0.35) 0%, transparent 70%);
  top: -150px; right: -100px;
}
.orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(200, 180, 255, 0.3) 0%, transparent 70%);
  bottom: 10%; left: -120px;
}
.orb-3 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(180, 160, 250, 0.2) 0%, transparent 70%);
  top: 40%; right: 5%;
}

/* ============================
   Top Navigation
   ============================ */
.top-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
  pointer-events: none;
}
.top-nav.nav-scrolled {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border-bottom: 1px solid var(--glass-border);
  box-shadow: var(--shadow-sm);
}

.nav-inner {
  width: 100%;
  max-width: 1200px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  pointer-events: auto;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-bloom {
  position: relative;
}
.logo-bloom::before {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(123, 97, 255, 0.3), rgba(155, 135, 253, 0.1));
  filter: blur(8px);
}

.logo-icon {
  position: relative;
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 14px rgba(123, 97, 255, 0.35);
}

.logo-text {
  font-family: 'Outfit', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-link {
  padding: 8px 16px;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.nav-link:hover {
  color: var(--primary);
  background: rgba(123, 97, 255, 0.06);
}
.nav-link-active {
  color: var(--primary);
  background: rgba(123, 97, 255, 0.1);
  font-weight: 600;
}

.btn-glass {
  padding: 8px 20px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  color: var(--primary);
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: var(--shadow-sm);
}
.btn-glass:hover {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
  box-shadow: 0 4px 16px rgba(123, 97, 255, 0.35);
  transform: translateY(-1px);
}

/* ============================
   Sidebar — Glassmorphism
   ============================ */
.sidebar {
  width: 240px;
  flex-shrink: 0;
  position: fixed;
  top: 64px; left: 0; bottom: 0;
  z-index: 50;
  padding: 12px;
  transition: width var(--transition-slow);
}
.sidebar.collapsed {
  width: 80px;
}

.sidebar-glass {
  height: 100%;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: var(--shadow);
}

/* ---- Logo ---- */
.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 16px 12px;
  color: var(--text-primary);
  text-decoration: none;
  white-space: nowrap;
}
.collapsed .sidebar-logo {
  padding: 16px 0 12px;
  justify-content: center;
}
.logo-icon-sm {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 2px 10px rgba(123, 97, 255, 0.3);
}
.logo-text-sm {
  font-family: 'Outfit', sans-serif;
  font-size: 15px;
  font-weight: 700;
  transition: opacity 0.2s;
}
.collapsed .logo-text-sm { display: none; }

/* ---- Nav ---- */
.sidebar-nav {
  flex: 1;
  padding: 4px 10px;
  overflow-y: auto;
  overflow-x: hidden;
}
.collapsed .sidebar-nav { padding: 4px 8px; }

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  margin: 2px 0;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: all var(--transition-fast);
  position: relative;
  white-space: nowrap;
}
.collapsed .nav-item {
  padding: 10px 0;
  justify-content: center;
  gap: 0;
}

.nav-icon-wrap {
  width: 28px; height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.nav-item:hover {
  background: rgba(123, 97, 255, 0.08);
  color: var(--text-primary);
}
.nav-item:hover .nav-icon-wrap {
  background: rgba(123, 97, 255, 0.1);
  color: var(--primary);
}

.nav-item.nav-active {
  background: var(--bg-sidebar-active);
  color: var(--primary);
  font-weight: 600;
}
.nav-item.nav-active .nav-icon-wrap {
  background: rgba(123, 97, 255, 0.15);
  color: var(--primary);
}
.nav-item.nav-active::before {
  content: '';
  position: absolute;
  left: -10px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px; height: 18px;
  background: linear-gradient(180deg, var(--primary), var(--primary-light));
  border-radius: 0 3px 3px 0;
}
.collapsed .nav-item.nav-active::before {
  left: -8px;
}

/* Sub-item */
.nav-item.nav-sub {
  padding-left: 20px;
  font-size: 12px;
  margin-left: 6px;
}
.collapsed .nav-item.nav-sub {
  padding-left: 0;
  margin-left: 0;
  justify-content: center;
}

.collapsed .nav-item span { display: none; }

/* ---- Group ---- */
.nav-group {
  margin-bottom: 4px;
}
.collapsed .nav-group { margin-bottom: 2px; }

.group-label {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 7px 12px;
  border: none;
  background: none;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 6px;
  transition: color var(--transition-fast);
  font-family: inherit;
  text-align: left;
}
.group-label:hover { color: var(--text-secondary); }
.collapsed .group-label { display: none; }

.group-arrow {
  margin-left: auto;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  color: var(--text-muted);
  flex-shrink: 0;
}
.group-arrow.expanded { transform: rotate(180deg); }

.group-items {
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.25s ease;
  max-height: 800px;
  opacity: 1;
}
.group-items.collapsed { max-height: 0; opacity: 0; }

/* ---- Divider ---- */
.nav-divider {
  height: 1px;
  background: var(--divider);
  margin: 8px 10px;
  flex-shrink: 0;
}
.collapsed .nav-divider { margin: 8px 12px; }

/* ---- Footer ---- */
.sidebar-footer {
  padding: 10px 12px;
  border-top: 1px solid var(--divider);
}
.collapsed .sidebar-footer {
  padding: 10px 0;
  display: flex;
  justify-content: center;
}

.collapse-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 10px;
  border: none;
  border-radius: var(--radius-sm);
  background: none;
  color: var(--text-muted);
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.collapse-btn:hover {
  background: rgba(123, 97, 255, 0.06);
  color: var(--text-secondary);
}
.collapsed .collapse-btn {
  width: auto;
  padding: 8px;
  justify-content: center;
}
.collapsed .collapse-btn span { display: none; }

/* ============================
   Content
   ============================ */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 240px;
  margin-top: 64px;
  min-height: calc(100vh - 64px);
  transition: margin-left var(--transition-slow);
}
.sidebar.collapsed ~ .content {
  margin-left: 80px;
}

.content-header {
  padding: 28px 36px 20px;
}
.header-glass {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 20px 28px;
  box-shadow: var(--shadow);
}
.page-title {
  font-family: 'Outfit', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.3;
  letter-spacing: -0.3px;
}
.page-desc {
  margin-top: 4px;
  font-size: 13px;
  color: var(--text-muted);
}

.content-body {
  flex: 1;
  padding: 0 36px 36px;
}
.content-body.home {
  padding: 0;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ===== Modal ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(26, 21, 40, 0.35);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.modal-glass {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur-heavy);
  -webkit-backdrop-filter: var(--glass-blur-heavy);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 460px;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.modal-glass.modal-wide {
  max-width: 560px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px 16px;
  border-bottom: 1px solid var(--divider);
}
.modal-title {
  font-family: 'Outfit', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}
.modal-close {
  width: 32px; height: 32px;
  border: none;
  background: none;
  color: var(--text-muted);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}
.modal-close:hover {
  background: rgba(123, 97, 255, 0.08);
  color: var(--text-primary);
}

.modal-body {
  padding: 20px 24px 24px;
  overflow-y: auto;
}
.modal-desc {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.6;
  margin: 0 0 20px;
}

.modal-features {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: rgba(123, 97, 255, 0.04);
  border-radius: var(--radius);
  border: 1px solid var(--border-light);
}
.feature-icon {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, var(--primary), var(--primary-light));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}
.feature-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.feature-text strong {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}
.feature-text span {
  font-size: 12px;
  color: var(--text-muted);
}

.modal-action {
  display: flex;
  justify-content: center;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 24px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: 0 4px 16px rgba(123, 97, 255, 0.35);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(123, 97, 255, 0.45);
}

/* Site Grid */
.site-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.site-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: rgba(123, 97, 255, 0.03);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  text-decoration: none;
  transition: all var(--transition);
  cursor: pointer;
}
.site-card:hover {
  background: rgba(123, 97, 255, 0.07);
  border-color: rgba(123, 97, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
.site-icon {
  width: 40px; height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}
.site-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}
.site-info strong {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}
.site-info span {
  font-size: 12px;
  color: var(--text-muted);
}

.site-copy {
  margin-left: auto;
  color: var(--text-muted);
  opacity: 0;
  transition: opacity var(--transition-fast);
}
.site-card:hover .site-copy {
  opacity: 1;
}

.copy-tip {
  text-align: center;
  font-size: 13px;
  color: var(--primary);
  font-weight: 500;
  margin-top: 16px;
  animation: fade-in-up 0.2s ease;
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Modal transition */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.25s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
.modal-enter-active .modal-glass,
.modal-leave-active .modal-glass {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-enter-from .modal-glass,
.modal-leave-to .modal-glass {
  transform: scale(0.92) translateY(10px);
}

/* 响应式：小屏幕隐藏顶部导航的链接 */
@media (max-width: 768px) {
  .nav-links { display: none; }
  .modal-glass { max-width: 100%; }
  .site-grid { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .content { margin-left: 0; }
}
</style>
