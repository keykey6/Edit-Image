# 超级全能图像工具箱

纯本地运行的图像处理工具箱，涵盖 **45 个功能模块**，从基础编辑到智能分析。零云 API 依赖，完全免费开源。

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3.5 + TypeScript + Vite 8 + Element Plus 2 |
| 后端 | Python 3.12 + FastAPI + Uvicorn |
| 图像处理 | Pillow + OpenCV + rembg + imagehash + qrcode |
| 包管理 | pnpm (前端) / uv (后端) |

## 快速开始

```bash
# 后端
cd backend
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 9000 --reload

# 前端
cd frontend
pnpm install
pnpm dev
```

打开 http://localhost:5173 即可使用。

## 功能模块（10 类 · 45 模块）

| 分类 | 模块 |
|------|------|
| 图片调整 | 裁剪旋转、压缩、格式转换、圆角边框、图片信息、DPI设置 |
| 颜色与光影 | 调色滤镜、曲线调色、HSL调色、去雾提亮、直方图、色彩分析 |
| 艺术效果 | 素描漫画、阴影倒影、透视矫正 |
| 人像美化 | 证件照、AI抠图、换背景、人像美颜、老照片修复、证件照换装 |
| 安全与隐私 | 水印添加、水印去除、模糊打码、隐私擦除、图片加密 |
| 拼接与布局 | 拼图、切图、长图拼接、社交媒体配图 |
| 格式工具 | 分辨率放大、图片转PDF、图片转ICO |
| 生成与识别 | 二维码生成、二维码解码、条形码、文字转图片、表情包 |
| 智能分析 | 相似度对比、重复检测、质量评分、取色器 |
| 批量操作 | 批量处理、批量重命名、批量改尺寸、预设管理 |

## 项目结构

```
├── backend/                # FastAPI 后端
│   ├── main.py             # 入口，注册 45 个路由
│   ├── config.py           # 全局配置
│   ├── routers/            # 45 个功能模块路由
│   ├── services/           # 通用工具函数
│   └── uploads/            # 临时文件目录
├── frontend/               # Vue3 前端
│   ├── src/
│   │   ├── views/          # 46 个功能页面
│   │   ├── components/     # 7 个通用组件
│   │   ├── router/         # 路由（10 类分组）
│   │   ├── api/            # HTTP 层
│   │   ├── layouts/        # 布局组件
│   │   └── styles/         # 紫色主题样式
│   └── public/
└── docs/                   # 设计文档
    ├── ARCHITECTURE.md     # 完整架构文档
    └── design.md           # 原始需求文档
```

## 设计系统

- 主色 `#6C5CE7`（紫色），侧栏深色 `#0f172a`，内容区浅色 `#f8fafc`
- 约 35 个页面复用 ToolPage 组件，约 10 个复杂页面自管状态
- 统一 API 模式：`POST /api/{module}/process`

## 许可

MIT License
