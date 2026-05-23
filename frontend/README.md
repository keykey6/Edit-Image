# 超级全能图像工具箱 — 前端

Vue3 + Element Plus 前端，45 个图像处理功能页面。

## 技术栈

- Vue 3.5 + TypeScript + Vite 8
- Element Plus 2 + @element-plus/icons-vue
- pnpm

## 快速启动

```bash
# 安装依赖
pnpm install

# 启动开发服务器 (port 5173)
pnpm dev

# 构建生产版本
pnpm build
```

## 项目结构

```
修图-frontend/
├── src/
│   ├── main.ts                 # 入口
│   ├── App.vue                 # 根组件
│   ├── router/index.ts         # 45 条路由 + 10 类分组
│   ├── api/index.ts            # HTTP 层（axios → /api proxy）
│   ├── layouts/
│   │   └── MainLayout.vue      # 深色侧栏 + 内容区布局
│   ├── views/                  # 46 个功能页面
│   │   ├── CropRotate.vue      # ToolPage 模式（~35个页面）
│   │   ├── IdPhoto.vue         # 自定义模式（~10个页面）
│   │   └── ...
│   ├── components/             # 7 个通用组件
│   │   ├── ToolPage.vue        # 通用处理流程组件
│   │   ├── ImageUploader.vue   # 拖拽/粘贴/点击上传
│   │   ├── ImageCompare.vue    # 并排/滑动双模式对比
│   │   └── ...
│   └── styles/global.css       # 紫色主题全局样式
└── vite.config.ts              # Vite + /api proxy → :9000
```

## 设计系统

- 主色：`#6C5CE7`（紫色）
- 侧栏：深色背景 `#0f172a`
- 内容区：浅色背景 `#f8fafc`
- 卡片：白色 + 圆角 14px + 微妙阴影

## 视图模式

- **ToolPage 模式**（约 35 个页面）：通过 ToolPage 组件复用上传→处理→对比→下载流程
- **自定义模式**（约 10 个页面）：多文件、双图对比、JSON 展示等复杂交互自管状态
