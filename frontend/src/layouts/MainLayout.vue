<template>
  <div class="layout">
    <aside class="sidebar">
      <router-link to="/" class="sidebar-logo">
        <div class="logo-icon">
          <el-icon :size="22"><PictureFilled /></el-icon>
        </div>
        <span class="logo-text">修图工具箱</span>
      </router-link>

      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item nav-home" active-class="nav-active" exact-active-class="nav-active">
          <el-icon :size="16"><HomeFilled /></el-icon>
          <span>首页</span>
        </router-link>
        <div v-for="cat in categories" :key="cat.key" class="nav-group">
          <button class="group-label" @click="toggleCat(cat.key)">
            <span class="group-dot" />
            <span>{{ cat.label }}</span>
            <el-icon class="group-arrow" :class="{ expanded: openCats.has(cat.key) }">
              <ArrowDown />
            </el-icon>
          </button>
          <div class="group-items" :class="{ collapsed: !openCats.has(cat.key) }">
            <router-link
              v-for="item in cat.items"
              :key="item.path"
              :to="item.path"
              class="nav-item"
              active-class="nav-active"
            >
              <el-icon :size="16"><component :is="item.icon" /></el-icon>
              <span>{{ item.title }}</span>
            </router-link>
          </div>
        </div>
      </nav>

      <div class="sidebar-footer">
        <span>v2.0</span>
      </div>
    </aside>

    <main class="content">
      <header class="content-header">
        <h1 class="page-title">{{ currentTitle }}</h1>
        <p class="page-desc">{{ currentDesc }}</p>
      </header>
      <div class="content-body">
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
import { computed, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { ROUTES, CATEGORIES, DESCRIPTIONS } from '@/router'

const route = useRoute()

const openCats = reactive(new Set(Object.keys(CATEGORIES)))

function toggleCat(key: string) {
  if (openCats.has(key)) { openCats.delete(key) } else { openCats.add(key) }
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
.layout { display: flex; min-height: 100vh; }

/* ---- Sidebar ---- */
.sidebar {
  width: 250px;
  background: var(--sidebar-bg);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 20px;
  color: #fff;
  text-decoration: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.logo-icon {
  width: 36px; height: 36px;
  background: var(--primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.logo-text { font-size: 16px; font-weight: 700; }

.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  overflow-y: auto;
}

/* Group header */
.nav-group { margin-bottom: 18px; }

.group-label {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 6px 10px;
  margin-bottom: 4px;
  border: none;
  background: none;
  color: rgba(255, 255, 255, 0.35);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.6px;
  cursor: pointer;
  border-radius: 6px;
  transition: color 0.2s;
}
.group-label:hover { color: rgba(255, 255, 255, 0.6); }

.group-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  flex-shrink: 0;
}
.group-arrow {
  margin-left: auto;
  font-size: 12px;
  transition: transform 0.2s;
  opacity: 0.6;
}
.group-arrow.expanded { transform: rotate(180deg); }

/* Items */
.group-items {
  overflow: hidden;
  transition: max-height 0.25s ease, opacity 0.2s ease;
  max-height: 500px;
  opacity: 1;
}
.group-items.collapsed { max-height: 0; opacity: 0; }

.nav-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 12px 8px 16px;
  margin: 1px 6px 1px 8px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.55);
  text-decoration: none;
  font-size: 13px;
  transition: all 0.15s;
  position: relative;
}
.nav-item::before {
  content: '';
  position: absolute;
  left: 4px;
  width: 4px; height: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  opacity: 0;
  transition: opacity 0.15s, background 0.15s;
}
.nav-item:hover { background: var(--sidebar-hover); color: rgba(255, 255, 255, 0.85); }
.nav-item:hover::before { opacity: 1; }
.nav-item.nav-active {
  background: var(--sidebar-active);
  color: #c4b5fd;
  font-weight: 500;
}
.nav-item.nav-active::before {
  opacity: 1;
  background: var(--primary-light);
  width: 3px; height: 16px;
  border-radius: 2px;
  left: 5px;
}

.sidebar-footer {
  padding: 14px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.2);
  font-size: 11px;
  text-align: center;
}

/* ---- Content ---- */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background: var(--content-bg);
}

.content-header {
  padding: 24px 36px 20px;
  background: var(--card-bg);
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

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
