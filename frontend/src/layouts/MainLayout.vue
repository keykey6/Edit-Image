<template>
  <div class="layout">
    <aside class="sidebar" :class="{ collapsed }">
      <!-- Logo -->
      <router-link to="/" class="sidebar-logo">
        <div class="logo-icon">
          <el-icon :size="20"><PictureFilled /></el-icon>
        </div>
        <span class="logo-text">修图工具箱</span>
      </router-link>

      <!-- Nav -->
      <nav class="sidebar-nav">
        <!-- Home -->
        <router-link to="/" class="nav-item" active-class="nav-active" exact-active-class="nav-active">
          <el-icon :size="20"><HomeFilled /></el-icon>
          <span>首页</span>
        </router-link>

        <div class="nav-divider" />

        <!-- Categories -->
        <div v-for="cat in categories" :key="cat.key" class="nav-group">
          <button class="group-label" @click="toggleCat(cat.key)">
            <span>{{ cat.label }}</span>
            <el-icon class="group-arrow" :class="{ expanded: openCats.has(cat.key) }" :size="14">
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
              <el-icon :size="18"><component :is="item.icon" /></el-icon>
              <span>{{ item.title }}</span>
            </router-link>
          </div>
        </div>
      </nav>

      <!-- Footer -->
      <div class="sidebar-footer">
        <button class="collapse-btn" @click="collapsed = !collapsed">
          <el-icon :size="16">
            <DArrowLeft v-if="collapsed" />
            <DArrowRight v-else />
          </el-icon>
          <span>收起侧边栏</span>
        </button>
      </div>
    </aside>

    <main class="content">
      <header v-if="!isHome" class="content-header">
        <h1 class="page-title">{{ currentTitle }}</h1>
        <p class="page-desc">{{ currentDesc }}</p>
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
import { computed, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ROUTES, CATEGORIES, DESCRIPTIONS } from '@/router'

const route = useRoute()

const collapsed = ref(false)
const openCats = reactive(new Set<string>())

function toggleCat(key: string) {
  if (openCats.has(key)) { openCats.delete(key) } else { openCats.add(key) }
}

const isHome = computed(() => route.path === '/')

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
.layout { display: flex; min-height: 100vh; }

/* ============================
   Sidebar — Dark theme
   ============================ */
.sidebar {
  width: 220px;
  background: #0F172A;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
  overflow-x: hidden;
  transition: width 0.25s ease;
}

.sidebar.collapsed {
  width: 72px;
}

/* ---- Logo ---- */
.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 16px;
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid #1E293B;
  white-space: nowrap;
}
.collapsed .sidebar-logo {
  padding: 16px 0;
  justify-content: center;
}
.logo-icon {
  width: 32px; height: 32px;
  background: var(--primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}
.logo-text {
  font-size: 16px;
  font-weight: 700;
  transition: opacity 0.2s;
}
.collapsed .logo-text { display: none; }

/* ---- Nav ---- */
.sidebar-nav {
  flex: 1;
  padding: 8px 8px;
  overflow-y: auto;
}
.collapsed .sidebar-nav { padding: 8px 6px; }

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  margin: 1px 0;
  border-radius: 8px;
  color: #94A3B8;
  text-decoration: none;
  font-size: 13px;
  font-weight: 400;
  transition: all 0.15s;
  position: relative;
  white-space: nowrap;
}
.collapsed .nav-item {
  padding: 10px 0;
  justify-content: center;
  gap: 0;
  border-radius: 8px;
}

.nav-item:hover {
  background: #1E293B;
  color: #E2E8F0;
}

.nav-item.nav-active {
  background: #1E293B;
  color: #fff;
  font-weight: 500;
}
.nav-item.nav-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6px;
  bottom: 6px;
  width: 3px;
  background: #7C3AED;
  border-radius: 0 2px 2px 0;
}
.collapsed .nav-item.nav-active::before {
  left: 2px;
  top: 8px;
  bottom: 8px;
}

/* Sub-item indent */
.nav-item.nav-sub {
  padding-left: 24px;
  font-size: 13px;
  margin-left: 8px;
  border-left: 2px solid transparent;
  border-radius: 0 8px 8px 0;
}
.collapsed .nav-item.nav-sub {
  padding-left: 0;
  margin-left: 0;
  border-left: none;
  justify-content: center;
}

.nav-item.nav-sub.nav-active {
  border-left-color: #334155;
}

/* Hide text in collapsed */
.collapsed .nav-item span { display: none; }
.collapsed .nav-item .el-icon { margin: 0; }

/* ---- Group ---- */
.nav-group {
  margin-bottom: 2px;
}
.collapsed .nav-group { margin-bottom: 0; }

.group-label {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 8px 12px;
  border: none;
  background: none;
  color: #64748B;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  cursor: pointer;
  border-radius: 6px;
  transition: color 0.15s;
  font-family: inherit;
  text-align: left;
}
.group-label:hover { color: #94A3B8; }
.collapsed .group-label { display: none; }

.group-arrow {
  margin-left: auto;
  transition: transform 0.2s;
  color: #64748B;
  flex-shrink: 0;
}
.group-arrow.expanded { transform: rotate(180deg); }

.group-items {
  overflow: hidden;
  transition: max-height 0.25s ease, opacity 0.2s ease;
  max-height: 600px;
  opacity: 1;
}
.group-items.collapsed { max-height: 0; opacity: 0; }

/* ---- Divider ---- */
.nav-divider {
  height: 1px;
  background: #1E293B;
  margin: 6px 8px;
  flex-shrink: 0;
}
.collapsed .nav-divider { margin: 8px 12px; }

/* ---- Footer ---- */
.sidebar-footer {
  padding: 10px 12px;
  border-top: 1px solid #1E293B;
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
  border-radius: 6px;
  background: none;
  color: #64748B;
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s;
}
.collapse-btn:hover { background: #1E293B; color: #94A3B8; }
.collapsed .collapse-btn {
  width: auto;
  padding: 8px;
  justify-content: center;
}

/* ============================
   Content
   ============================ */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background: #FFFFFF;
}

.content-header {
  padding: 24px 36px 20px;
  background: #fff;
  border-bottom: 1px solid var(--border-color);
}
.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.3;
}
.page-desc {
  margin-top: 4px;
  font-size: 13px;
  color: var(--text-muted);
}

.content-body {
  flex: 1;
  padding: 28px 36px;
}
.content-body.home {
  padding: 0;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
