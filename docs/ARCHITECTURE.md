# 超级全能图像工具箱 — 架构文档

## 1. 项目概览

**超级全能图像工具箱** 是一个纯本地运行的图像处理工具箱，涵盖 45 个功能模块。前端 Vue 3 + Element Plus，后端 FastAPI，所有图像处理功能基于 Pillow/OpenCV 纯 Python 实现，零云 API 依赖。

| 属性 | 值 |
|------|-----|
| 后端框架 | FastAPI + Uvicorn (port 9000) |
| 前端框架 | Vue 3.5 + TypeScript + Vite + Element Plus 2 (port 5173) |
| Python | >= 3.12 |
| 包管理器 | uv (后端) / pnpm (前端) |
| 数据库 | 无（JSON 文件持久化预设） |
| 文件存储 | `backend/uploads/` 临时目录（处理完即清理） |
| 内容审核 | OpenCV Haar Cascade 人脸 + YCrCb 肤色分析 |
| 智能搜索 | jieba 分词 + TF-IDF 向量化 |

---

## 2. 项目结构

```
super-image-toolbox/
├── backend/                         # FastAPI 后端
│   ├── main.py                      # 应用入口，注册全部路由
│   ├── config.py                    # 全局配置
│   ├── pyproject.toml               # Python 依赖声明 (uv)
│   ├── uv.lock                      # 依赖锁定文件
│   ├── routers/                     # 45 个功能模块路由
│   │   ├── __init__.py
│   │   ├── crop_rotate.py           # 裁剪旋转
│   │   ├── compress.py              # 图片压缩
│   │   ├── format_convert.py        # 格式转换
│   │   ├── rounded_border.py        # 圆角边框
│   │   ├── image_info.py            # 图片信息
│   │   ├── dpi.py                   # DPI设置
│   │   ├── color_filter.py          # 调色滤镜
│   │   ├── curve.py                 # 曲线调色
│   │   ├── hsl.py                   # HSL调色
│   │   ├── dehaze.py                # 去雾提亮
│   │   ├── histogram.py             # 图片直方图
│   │   ├── color_analysis.py        # 色彩分析
│   │   ├── sketch_effect.py         # 素描漫画
│   │   ├── shadow.py                # 阴影倒影
│   │   ├── perspective.py           # 透视矫正
│   │   ├── id_photo.py              # 证件照
│   │   ├── remove_bg.py             # AI抠图
│   │   ├── change_bg.py             # 换背景
│   │   ├── face_beauty.py           # 人像美颜
│   │   ├── photo_restore.py         # 老照片修复
│   │   ├── suit_change.py           # 证件照换装
│   │   ├── watermark_add.py         # 水印添加
│   │   ├── watermark_remove.py      # 水印去除
│   │   ├── blur_mosaic.py           # 模糊打码
│   │   ├── privacy_erase.py         # 隐私擦除
│   │   ├── encrypt.py               # 图片加密
│   │   ├── photo_collage.py         # 拼图
│   │   ├── grid_split.py            # 切图
│   │   ├── long_stitch.py           # 长图拼接
│   │   ├── social_media.py          # 社交媒体配图
│   │   ├── super_res.py             # 分辨率放大
│   │   ├── to_pdf.py                # 图片转PDF
│   │   ├── to_ico.py                # 图片转ICO
│   │   ├── qrcode_gen.py            # 二维码生成
│   │   ├── qr_decode.py             # 二维码解码
│   │   ├── barcode.py               # 条形码生成
│   │   ├── text_to_image.py         # 文字转图片
│   │   ├── meme.py                  # 表情包制作
│   │   ├── similarity.py            # 相似度对比
│   │   ├── duplicate.py             # 重复检测
│   │   ├── quality_score.py         # 质量评分
│   │   ├── color_picker.py          # 取色器
│   │   ├── batch_process.py         # 批量处理
│   │   ├── batch_rename.py          # 批量重命名
│   │   ├── batch_resize.py          # 批量改尺寸
│   │   ├── preset_save.py           # 处理预设
│   │   └── smart_search.py          # AI智能搜索
│   ├── services/                    # 共享服务层
│   │   ├── __init__.py
│   │   ├── image_utils.py           # 图片读写、参数解析、临时文件管理
│   │   ├── content_moderation.py    # 内容安全审核
│   │   ├── embedding.py             # jieba + TF-IDF 文本向量化
│   │   └── tool_descriptions.py     # 45 个工具搜索元数据
│   └── uploads/                     # 临时文件目录
│       └── .gitkeep
├── frontend/                        # Vue 3 前端
│   ├── index.html                   # HTML 入口
│   ├── vite.config.ts               # Vite 配置 + /api 代理
│   ├── package.json                 # Node 依赖 (pnpm)
│   ├── pnpm-lock.yaml               # 依赖锁定文件
│   ├── tsconfig.json                # TypeScript 配置
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   └── src/
│       ├── main.ts                  # Vue 应用入口
│       ├── App.vue                  # 根组件
│       ├── api/index.ts             # HTTP 请求层 (axios)
│       ├── router/index.ts          # 45 条路由 + 10 类分组 + 分类元数据
│       ├── layouts/
│       │   └── MainLayout.vue       # 暗色侧栏 + 内容区布局
│       ├── components/
│       │   ├── ToolPage.vue         # 通用处理流程组件 (~35 个视图复用)
│       │   ├── ImageUploader.vue    # 拖拽/粘贴/点击上传
│       │   ├── ImageCompare.vue     # 并排/滑动双模式对比
│       │   ├── ParamSlider.vue      # 参数滑块
│       │   ├── ColorPicker.vue      # 颜色选择器
│       │   ├── DownloadButton.vue   # 下载按钮
│       │   └── EmptyState.vue       # 空状态占位
│       ├── views/                   # 46 个功能页面
│       │   ├── HomePage.vue         # 首页 (AI 智能搜索)
│       │   └── ...                  # 45 个工具页面
│       └── styles/
│           └── global.css           # 全局主题 CSS 变量
└── docs/                            # 项目文档
    ├── ARCHITECTURE.md              # 本架构文档
    └── superpowers/                 # 功能设计文档与实现计划
        ├── specs/
        └── plans/
```

---

## 3. API 设计

### 3.1 统一端点模式

全部 45 个模块遵循同一约定：

```
POST /api/{module}/process
Content-Type: multipart/form-data

字段:
  file        — 单文件 (image/*)
  files       — 多文件 (批量操作)
  params      — JSON 字符串, 如 '{"quality": 80, "format": "jpg"}'
```

### 3.2 响应类型

| 类型 | Content-Type | 示例模块 |
|------|-------------|---------|
| 图片 | `image/png` | compress, color_filter, dehaze 等 ~35 个 |
| JSON | `application/json` | similarity, quality_score, color_analysis, qr_decode, color_picker, preset_save |
| ZIP | `application/zip` | batch_process, batch_rename, batch_resize |

### 3.3 后端路由器模板

```python
# routers/example.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from services.image_utils import save_upload, cleanup_temp, parse_params, save_image

router = APIRouter(prefix="/api/example", tags=["示例"])

@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    fpath, file_id = save_upload(file)
    try:
        img = Image.open(fpath).convert("RGB")
        # ... 处理逻辑 ...
        out = save_image(result, file_id, "png")
        return FileResponse(out, media_type="image/png")
    finally:
        cleanup_temp(fpath)
```

### 3.4 前端 API 层

```typescript
// src/api/index.ts
// 图片/二进制 → responseType: 'blob'
api.post(`/${module}/process`, formData, { responseType: 'blob' })

// JSON → 无 responseType
api.post(`/${module}/process`, formData)
```

Vite 开发服务器通过 `vite.config.ts` 的 proxy 将 `/api` 转发到 `localhost:9000`。

---

## 4. 功能模块技术矩阵

### 4.1 图片调整 (basic)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| crop_rotate | Pillow | PIL rotate + crop, 按比例/自由裁剪, 任意角度旋转翻转 |
| compress | Pillow | PIL save(quality=), JPEG/PNG/WebP 压缩 |
| format_convert | Pillow | PIL 格式互转, 支持 JPG/PNG/WebP/BMP |
| rounded_border | Pillow + numpy | ImageDraw 圆角蒙版 + 自定义圆角半径 |
| image_info | Pillow + os.stat | EXIF 解析, 拍摄参数/GPS/相机型号提取 |
| dpi | Pillow | save(dpi=) 修改打印分辨率 |

### 4.2 颜色与光影 (color)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| color_filter | Pillow + numpy | numpy 矩阵运算 + ImageEnhance 增强 |
| curve | numpy | interp 构建 RGB LUT 映射 |
| hsl | OpenCV | BGR ↔ HLS 色彩空间转换 |
| dehaze | OpenCV | CLAHE 自适应直方图均衡 |
| histogram | Pillow + numpy | 像素统计 + ImageDraw 绘制直方图 |
| color_analysis | scikit-learn | KMeans 聚类提取主色调 |

### 4.3 艺术效果 (effects)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| sketch_effect | OpenCV | Canny 边缘检测 / 自适应阈值素描 |
| shadow | Pillow | 翻转 + alpha 渐变融合 |
| perspective | OpenCV | getPerspectiveTransform + warpPerspective |

### 4.4 人像美化 (portrait)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| id_photo | OpenCV | Haar Cascade 人脸检测 + 证件照尺寸裁剪 |
| remove_bg | rembg[cpu] | U2Net 显著性检测模型 |
| change_bg | rembg + Pillow | 抠图 + PIL 背景合成 |
| face_beauty | OpenCV | 双边滤波磨皮 + 锐化 |
| photo_restore | OpenCV | 形态学划痕检测 + fastNlMeansDenoising + CLAHE + 灰度世界白平衡 |
| suit_change | rembg + Pillow | 抠图 + V领西装模板合成 |

### 4.5 安全与隐私 (privacy)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| watermark_add | Pillow | ImageDraw 文字/图片叠加, 批量水印 |
| watermark_remove | OpenCV | inpaint 修复 |
| blur_mosaic | OpenCV | Haar 人脸 + 车牌检测 + GaussianBlur |
| privacy_erase | Pillow | EXIF 清理 + 图像数据重建 |
| encrypt | pycryptodome | AES-256-CBC 文件字节流加密 |

### 4.6 拼接与布局 (layout)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| photo_collage | Pillow | 网格布局拼接 |
| grid_split | Pillow | crop 等分切割 (九宫格等) |
| long_stitch | Pillow | 纵向/横向拼接, 滚动截图合并 |
| social_media | Pillow | 按比例居中裁剪, 各平台尺寸适配 |

### 4.7 格式工具 (convert)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| super_res | OpenCV | resize INTER_CUBIC 插值放大 |
| to_pdf | img2pdf | 多图转单 PDF |
| to_ico | Pillow | 多尺寸 ICO 保存 |

### 4.8 生成与识别 (generate)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| qrcode_gen | qrcode | QR 码生成, 支持 URL/文本/WiFi |
| qr_decode | pyzbar | QR/条形码解码 |
| barcode | python-barcode | 商品条码/ISBN 生成 |
| text_to_image | Pillow | ImageDraw 文字渲染 + 自动换行 |
| meme | Pillow | 顶部/底部描边文字叠加 |

### 4.9 智能分析 (analysis)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| similarity | imagehash | 感知哈希 (pHash/aHash/dHash/wHash) + 汉明距离 |
| duplicate | imagehash | 批量哈希 + 汉明距离分组去重 |
| quality_score | OpenCV + numpy | Laplacian 方差 + 噪点估计 + 色彩丰富度 |
| color_picker | Pillow | getpixel 像素/区域颜色提取 |

### 4.10 批量操作 (batch)

| 模块 | 技术栈 | 关键算法 |
|------|--------|---------|
| batch_process | Pillow | 5 种操作 (调色/滤镜/水印/裁切/压缩) → ZIP |
| batch_rename | 标准库 | 模板命名 + 序号 padding → ZIP |
| batch_resize | Pillow | cover/contain/stretch 三模式 → ZIP |
| preset_save | 标准库 json | JSON 文件 CRUD, 方案持久化 |

---

## 5. 前端架构

### 5.1 路由设计

全部路由集中在 `src/router/index.ts`，含 10 类分组：

```typescript
export const ROUTES = [
  {
    path: '/crop-rotate',
    name: 'CropRotate',
    component: () => import('@/views/CropRotate.vue'),
    meta: { title: '裁剪旋转', icon: 'Crop', category: 'basic' }
  },
  // ... 共 45 条路由
]
```

- `meta.icon` — Element Plus 图标名，侧边栏渲染
- `meta.category` — 分类键，侧边栏分组依据
- 首页 `/` 路由至 HomePage (AI 智能搜索)

### 5.2 组件层级

```
App.vue
 └── MainLayout.vue (暗色侧栏 + 内容区)
      ├── 侧栏: 分类折叠导航, 展开 220px / 收起 72px
      └── <router-view>
           ├── ToolPage.vue           ← ~35 个视图复用
           │    ├── ImageUploader     (拖拽/粘贴/点击)
           │    ├── [slot:params]     (各页面自定义参数)
           │    ├── ImageCompare      (并排/滑动双模式)
           │    └── DownloadButton
           │
           └── 自定义视图             ← ~11 个复杂页面自管状态
                ├── ImageUploader
                ├── ParamSlider
                └── ColorPicker
```

### 5.3 视图模式

**模式 A: ToolPage 包装** (~35 个页面)

```vue
<template>
  <ToolPage module="compress" :params="params">
    <template #params>
      <el-slider v-model="params.quality" :min="1" :max="100" />
    </template>
  </ToolPage>
</template>
```

ToolPage 自动处理上传 → 处理 → 进度 → 对比 → 下载全流程。

**模式 B: 独立实现** (~11 个页面)

自管状态的页面: IdPhoto, ChangeBg, PhotoCollage, GridSplit, BatchProcess, LongStitch, ToPdf, BatchRename, BatchResize, Similarity, Duplicate, PresetSave, QrDecode, ColorPickerView, ColorAnalysis, QualityScore.

适用场景: 多文件上传、双图对比、JSON 展示、特殊交互流程。

### 5.4 设计系统

```css
:root {
  --primary: #7C3AED;           /* 品牌紫 */
  --primary-dark: #6D28D9;      /* 深紫 (hover/active) */
  --primary-light: #A78BFA;     /* 浅紫 */
  --primary-bg: rgba(124, 58, 237, 0.08);  /* 紫色背景 */
  --sidebar-bg: #0F172A;        /* 侧栏深蓝黑 */
  --sidebar-hover: #1E293B;     /* 侧栏悬浮 */
  --sidebar-active: rgba(124, 58, 237, 0.12);  /* 侧栏激活 */
  --sidebar-text: #94A3B8;      /* 侧栏文字 */
  --sidebar-text-active: #FFFFFF;  /* 侧栏激活文字 */
  --content-bg: #FFFFFF;        /* 内容区白色 */
  --border-color: #E2E8F0;      /* 边框 */
  --radius: 14px;               /* 圆角 */
}
```

侧栏设计：展开 220px，收缩 72px (仅图标)，分类默认折叠。激活项 3px 左侧 `#7C3AED` 竖线 + `#1E293B` 背景。紫色通过 CSS 变量注入 Element Plus 组件。

---

## 6. 智能搜索系统

### 6.1 架构

```
用户自然语言输入
     │
     ▼
┌─────────────────────────┐
│  jieba 分词 + TF-IDF     │   后端启动时预计算 45 个工具的
│  向量化查询文本           │   search_text 向量索引
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  余弦相似度计算           │   query_vec · tool_embeddings
│  (归一化点积)             │   返回 Top-N 匹配结果
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  结果过滤 (score ≥ 0.05) │   返回工具名、路径、
│  返回 JSON 结果列表       │   分类、匹配分数
└─────────────────────────┘
```

### 6.2 实现要点

- **词表构建**: 对 45 个工具的 `search_text` (中文关键词 + 场景描述) 进行 jieba 分词，构建 TF-IDF 词表
- **向量编码**: 每个工具描述编码为 TF-IDF 稀疏向量
- **查询匹配**: 用户中文查询 → jieba 分词 → TF-IDF 编码 → 与 45 个工具向量计算余弦相似度
- **索引预热**: 应用启动时 (`@router.on_event("startup")`) 构建索引，失败标记未就绪
- **容错**: 搜索服务未就绪返回 503，提示稍后重试

### 6.3 工具搜索元数据

每个工具在 `services/tool_descriptions.py` 中维护搜索文本，包含功能名、关键词、使用场景：

```python
("/remove-bg", "AI抠图", "Scissor", "portrait",
 "AI抠图 去除背景 背景消除 智能抠图 一键去背景 人物抠图 商品抠图 透明背景 把背景去掉 去掉背景"),
```

---

## 7. 内容安全审核

### 7.1 审核流程

```
上传图片
   │
   ▼
人脸检测 (Haar Cascade)
   │
   ├── 检测到人脸 → ✅ 放行 (正常肖像)
   │
   └── 无人脸
        │
        ▼
      肤色分析 (YCrCb)
        │
        ├── 肤色区域 < 3 个显著块 → ✅ 放行
        │
        └── 肤色区域 ≥ 3 个显著块
             │
             ▼
           血色检测 (HSV)
             │
             ├── 血色 < 12% 且连通性 < 25% → ✅ 放行
             │
             └── 血色 ≥ 12% 且连通性 ≥ 25% → ❌ 拦截
```

### 7.2 关键技术

- **人脸优先**: 检测到人脸直接放行，防止正常肖像被误拦
- **肤色检测**: YCrCb 色彩空间阈值，统计显著肤色区域数量
- **血色检测**: HSV 色彩空间红色范围 + 连通区域分析，区分分散的红色物体与集中的血液/暴力画面
- **中文路径兼容**: 使用 PIL 读取图片 (避免 cv2.imread Unicode 问题)，转为 numpy array 再给 OpenCV 处理

### 7.3 集成方式

通过 `services/image_utils.py` 的 `save_upload()` 统一拦截，`moderate_content` 参数默认开启。审核不通过会删除临时文件并返回 HTTP 400。

---

## 8. 关键设计决策

| 决策 | 原因 |
|------|------|
| 无数据库 | 纯工具型应用无持久化需求，预设用 JSON 文件 |
| 统一 API 端点 | `POST /api/{module}/process` 统一接口，前端零学习成本 |
| 纯 Python 实现 | 零外部 API 依赖，完全离线可用 |
| jieba + TF-IDF 搜索 | 纯本地中文分词 + 向量检索，无需 ONNX 模型或云 API |
| rembg CPU 版 | 无需 GPU，抠图效果优于 OpenCV GrabCut |
| OpenCV Haar Cascade | 人脸检测，避免 mediapipe 同名 PyPI 包冲突 |
| PIL 替代 cv2.imread/imwrite | OpenCV C++ 不支持中文路径 |
| 内容审核本地化 | 人脸 + 肤色 + 血色三阶段检测，无需外部审查 API |
| 灰度世界白平衡 | 老照片修复的白平衡算法，分别校正 A/B 通道均值到 128 |
| 形态学划痕检测 | 顶帽 + 黑帽运算仅检测细线划痕，避免 Canny 破坏面部细节 |
| CSS 变量主题 | 全局统一配色，一处修改全局生效 |
| ToolPage 组件复用 | ~70% 页面复用，减少重复代码 |
| 分类折叠暗色侧栏 | 45 个入口平铺不可用，10 类折叠导航 + 暗色主题 |

---

## 9. 已知局限

| 局限 | 说明 |
|------|------|
| 人脸检测精度 | OpenCV Haar Cascade 不如深度学习方案 (MTCNN/RetinaFace) |
| 老照片修复 | CLAHE + 去噪效果有限，真实修复需 GAN 模型 |
| 抠图速度 | rembg CPU 推理单张 ~2-5 秒 |
| 超分辨率 | INTER_CUBIC 插值是简单放大，非 AI 超分 |
| 换装效果 | 仅 V 领模板合成，非真实换装 |
| 中文搜索精度 | TF-IDF 基于词频匹配，非语义理解 |
| 无认证机制 | 仅适用于本地/可信环境 |
| 无国际化 | 仅中文 UI |
| 无自动化测试 | 当前无单元测试或集成测试 |

---

## 10. 扩展指南

### 10.1 添加新功能模块

**后端 (4 步):**

1. 在 `backend/routers/` 下创建 `new_module.py`，按路由器模板实现
2. 在 `backend/main.py` 中 import 并加入 `routers` 列表
3. 在 `backend/services/tool_descriptions.py` 的 `TOOLS` 列表中添加搜索元数据
4. 如需新依赖: `cd backend && uv add <package>`

**前端 (3 步):**

1. 在 `frontend/src/views/` 下创建视图 (优先复用 ToolPage)
2. 在 `frontend/src/router/index.ts` 的 `ROUTES` 中添加路由
3. 确保 `meta.category` 分配到正确的分类

### 10.2 添加新依赖需评估

- 是否纯 Python? (避免 C++ 编译依赖降低可移植性)
- 安装体积多大? (>100MB 需评估收益)
- 是否需要 GPU? (优先 CPU-only 方案)
- 是否支持中文路径? (OpenCV 的 C++ 层不支持)
