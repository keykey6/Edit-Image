# 超级全能图像工具箱

纯本地运行的图像处理工具箱，涵盖 **45 个功能模块**，覆盖图片编辑、人像美化、格式转换、智能分析等全部场景。零云 API 依赖，完全免费开源。

## 功能模块（10 类 · 45 模块）

| 分类 | 模块 |
|------|------|
| **图片调整** | 裁剪旋转、图片压缩、格式转换、圆角边框、图片信息、DPI设置 |
| **颜色与光影** | 调色滤镜、曲线调色、HSL调色、去雾提亮、图片直方图、色彩分析 |
| **艺术效果** | 素描漫画、阴影倒影、透视矫正 |
| **人像美化** | 证件照、AI抠图、换背景、人像美颜、老照片修复、证件照换装 |
| **安全与隐私** | 水印添加、水印去除、模糊打码、隐私擦除、图片加密 |
| **拼接与布局** | 拼图、切图、长图拼接、社交媒体配图 |
| **格式工具** | 分辨率放大、图片转PDF、图片转ICO |
| **生成与识别** | 二维码生成、二维码解码、条形码生成、文字转图片、表情包制作 |
| **智能分析** | 相似度对比、重复检测、质量评分、取色器 |
| **批量操作** | 批量处理、批量重命名、批量改尺寸、处理预设 |

### 特色能力

- **AI 智能搜索** — 自然语言描述需求，自动匹配最合适的工具（jieba + TF-IDF 中文语义搜索）
- **内容安全审核** — 本地人脸检测 + 肤色分析，自动拦截不当内容
- **暗色侧栏 UI** — 分类折叠导航，支持展开/收起双模式

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3.5 + TypeScript + Vite + Element Plus 2 |
| 后端 | Python 3.12 + FastAPI + Uvicorn |
| 图像处理 | Pillow + OpenCV + rembg + imagehash + qrcode |
| NLP | jieba 分词 + TF-IDF 向量化 |
| 包管理 | pnpm (前端) / uv (后端) |

## 快速开始

### 环境要求

- Python >= 3.12
- Node.js >= 18
- pnpm (推荐通过 `npm install -g pnpm` 安装)

### 启动后端

```bash
cd backend
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 9000 --reload
```

### 启动前端

```bash
cd frontend
pnpm install
pnpm dev
```

打开 <http://localhost:5173> 即可使用。

### 生产构建

```bash
cd frontend
pnpm build    # 产出到 frontend/dist/
```

## 项目结构

```
super-image-toolbox/
├── backend/                    # FastAPI 后端 (:9000)
│   ├── main.py                 # 入口，注册 45 个模块路由
│   ├── config.py               # 全局配置 (CORS、文件大小等)
│   ├── pyproject.toml          # Python 依赖 (uv)
│   ├── routers/                # 45 个功能模块路由
│   │   ├── crop_rotate.py      # 裁剪旋转
│   │   ├── compress.py         # 图片压缩
│   │   ├── ...                 # 各模块遵循统一 API 模式
│   │   └── smart_search.py     # AI 智能搜索
│   ├── services/               # 共享服务层
│   │   ├── image_utils.py      # 文件读写、参数解析
│   │   ├── content_moderation.py  # 内容安全审核
│   │   ├── embedding.py        # jieba + TF-IDF 向量化
│   │   └── tool_descriptions.py   # 45 个工具元数据
│   └── uploads/                # 临时文件 (自动清理)
├── frontend/                   # Vue 3 前端 (:5173)
│   ├── src/
│   │   ├── views/              # 46 个页面 (35 个复用 ToolPage)
│   │   ├── components/         # 7 个通用组件
│   │   ├── router/index.ts     # 路由定义 (10 类分组)
│   │   ├── api/index.ts        # HTTP 请求层
│   │   ├── layouts/            # 布局组件
│   │   └── styles/global.css   # 全局主题变量
│   ├── vite.config.ts          # Vite + /api 代理配置
│   └── public/                 # 静态资源
└── docs/                       # 文档
    ├── ARCHITECTURE.md         # 完整架构文档
    └── superpowers/            # 功能设计文档
```

## API 设计

所有模块遵循统一端点模式：

```
POST /api/{module}/process
Content-Type: multipart/form-data

字段:
  file    — 单文件上传 (image/*)
  files   — 多文件上传 (批量操作时)
  params  — JSON 字符串, 如 '{"quality": 80, "format": "jpg"}'
```

三种响应类型：
- `FileResponse` (image/png) — 图片处理结果
- `FileResponse` (application/zip) — 批量操作结果
- `JSONResponse` — 分析/检测结果

## 设计系统

| 变量 | 值 | 用途 |
|------|-----|------|
| `--primary` | `#7C3AED` | 主色调 |
| `--primary-dark` | `#6D28D9` | 深色变体 |
| `--primary-light` | `#A78BFA` | 浅色变体 |
| `--sidebar-bg` | `#0F172A` | 侧栏背景 |
| `--sidebar-text` | `#94A3B8` | 侧栏文字 |
| `--content-bg` | `#FFFFFF` | 内容区背景 |
| `--border-color` | `#E2E8F0` | 通用边框 |

## 扩展指南

### 添加新功能模块

**后端 (3 步):**
1. 在 `backend/routers/` 下创建 `new_module.py`，按模板实现 `/api/new-module/process`
2. 在 `backend/main.py` 中 import 并加入 `routers` 列表
3. 在 `backend/services/tool_descriptions.py` 中添加搜索元数据

**前端 (3 步):**
1. 在 `frontend/src/views/` 下创建视图 (复用 ToolPage 或独立实现)
2. 在 `frontend/src/router/index.ts` 的 `ROUTES` 中添加路由
3. 确保 `meta.category` 分配到正确的分类

## 许可

MIT License
