# 超级全能图像工具箱 — 架构文档

## 1. 项目概览

**超级全能图像工具箱** 是一个纯本地运行的图像处理工具箱，涵盖 45 个功能模块，从基础编辑到智能分析。前端 Vue3 + Element Plus，后端 FastAPI + Pillow/OpenCV，所有功能纯 Python 实现，零云 API 依赖。全部 45 个模块已完成开发。

| 属性 | 值 |
|------|-----|
| 后端框架 | FastAPI + Uvicorn (port 9000) |
| 前端框架 | Vue 3.5 + Vite 8 + Element Plus 2 (port 5173) |
| Python | >= 3.12 |
| 包管理器 | uv (后端) / pnpm (前端) |
| 数据库 | 无（JSON 文件持久化预设） |
| 文件存储 | `uploads/` 临时目录（处理完即清理） |
| 状态 | ✅ 全部 45 个模块已完成 |

---

## 2. 项目结构

```
修图-backend/                    修图-frontend/
├── main.py          ← 入口    ├── index.html
├── config.py        ← 配置    ├── vite.config.ts
├── pyproject.toml   ← 依赖    ├── package.json
├── routers/                   ├── src/
│   ├── crop_rotate.py         │   ├── main.ts          ← 入口
│   ├── compress.py            │   ├── App.vue          ← 根组件
│   ├── ...（共 45 个）        │   ├── api/index.ts    ← HTTP 层
│   └── preset_save.py         │   ├── router/index.ts  ← 路由定义
├── services/                  │   ├── layouts/
│   └── image_utils.py         │   │   └── MainLayout.vue
└── uploads/  ← 临时文件       │   ├── components/
                                │   │   ├── ToolPage.vue
                                │   │   ├── ImageUploader.vue
                                │   │   ├── ImageCompare.vue
                                │   │   ├── ParamSlider.vue
                                │   │   ├── ColorPicker.vue
                                │   │   ├── EmptyState.vue
                                │   │   └── DownloadButton.vue
                                │   ├── views/（45 个页面）
                                │   └── styles/global.css
```

---

## 3. API 设计

### 3.1 统一端点模式

所有 45 个模块遵循同一约定：

```
POST /api/{module}/process
Content-Type: multipart/form-data

字段:
  file        — 单文件（image/*）
  files       — 多文件（批量操作时使用）
  params      — JSON 字符串，如 '{"quality": 80, "format": "jpg"}'
```

### 3.2 三种响应类型

| 类型 | 返回 | 示例模块 |
|------|------|---------|
| **图片/二进制** | `FileResponse` (image/png) | compress, color_filter, dehaze 等 35 个模块 |
| **JSON** | `JSONResponse` | similarity, quality_score, color_analysis, qr_decode, color_picker, preset_save |
| **ZIP 包** | `FileResponse` (application/zip) | batch_process, batch_rename, batch_resize |

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
api.post(`/${module}/process`, formData, { responseType: 'blob' })  // → 图片/zip
api.post(`/${module}/process`, formData)                              // → JSON
```

通过 `vite.config.ts` 的 proxy 转发 `/api` 到 `localhost:9000`。

---

## 4. 功能模块全景

### 4.1 分类总览（10 类 · 45 模块）

| 分类 | 模块数 | 功能 |
|------|--------|------|
| **图片调整** | 6 | 裁剪旋转、压缩、格式转换、圆角边框、图片信息、DPI设置 |
| **颜色与光影** | 6 | 调色滤镜、曲线调色、HSL调色、去雾提亮、直方图、色彩分析 |
| **艺术效果** | 3 | 素描漫画、阴影倒影、透视矫正 |
| **人像美化** | 6 | 证件照、AI抠图、换背景、人像美颜、老照片修复、证件照换装 |
| **安全与隐私** | 5 | 水印添加、水印去除、模糊打码、隐私擦除、图片加密 |
| **拼接与布局** | 4 | 拼图、切图、长图拼接、社交媒体配图 |
| **格式工具** | 3 | 分辨率放大、图片转PDF、图片转ICO |
| **生成与识别** | 5 | 二维码生成、二维码解码、条形码生成、文字转图片、表情包 |
| **智能分析** | 4 | 相似度对比、重复检测、质量评分、取色器 |
| **批量操作** | 4 | 批量处理、批量重命名、批量改尺寸、预设管理 |

### 4.2 技术实现矩阵

| 模块 | 核心技术 | 依赖 |
|------|---------|------|
| crop_rotate | PIL rotate + crop | Pillow |
| compress | PIL save(quality=) | Pillow |
| format_convert | PIL 格式转换 | Pillow |
| rounded_border | PIL ImageDraw 圆角蒙版 | Pillow + numpy |
| image_info | PIL _getexif + os.stat | Pillow |
| dpi | PIL save(dpi=) | Pillow |
| color_filter | numpy 矩阵运算 + PIL ImageEnhance | Pillow + numpy |
| curve | numpy interp 构建 RGB LUT | numpy |
| hsl | OpenCV BGR↔HLS 色彩空间转换 | OpenCV |
| dehaze | CLAHE 自适应直方图均衡 | OpenCV |
| histogram | numpy 像素统计 + PIL ImageDraw | Pillow + numpy |
| color_analysis | sklearn KMeans 聚类提取主色调 | scikit-learn |
| sketch_effect | Canny 边缘检测 / 自适应阈值 | OpenCV |
| shadow | PIL 翻转 + alpha 渐变融合 | Pillow |
| perspective | OpenCV getPerspectiveTransform + warpPerspective | OpenCV |
| remove_bg | rembg (U2Net 模型) | rembg[cpu] |
| change_bg | rembg 抠图 + PIL 合成 | rembg + Pillow |
| id_photo | OpenCV Haar Cascade 人脸检测 | OpenCV |
| face_beauty | OpenCV 双边滤波 + 锐化 | OpenCV |
| photo_restore | CLAHE + 去噪 + 锐化 | OpenCV |
| suit_change | rembg 抠图 + PIL V领模板合成 | rembg + Pillow |
| watermark_add | PIL ImageDraw 文字/图片叠加 | Pillow |
| watermark_remove | OpenCV inpaint 修复 | OpenCV |
| blur_mosaic | OpenCV Haar 人脸检测 + GaussianBlur | OpenCV |
| privacy_erase | PIL info 清理 + 重建图像数据 | Pillow |
| encrypt | AES-256-CBC 加密文件字节流 | pycryptodome |
| photo_collage | PIL 网格布局拼接 | Pillow |
| grid_split | PIL crop 等分切割 | Pillow |
| long_stitch | PIL 纵向/横向拼接 | Pillow |
| social_media | PIL 按比例居中裁剪 | Pillow |
| super_res | OpenCV resize INTER_CUBIC 插值放大 | OpenCV |
| to_pdf | img2pdf 多图转单 PDF | img2pdf |
| to_ico | PIL 多尺寸 ICO 保存 | Pillow |
| qrcode_gen | qrcode 库生成 | qrcode |
| qr_decode | pyzbar 解码 QR/条形码 | pyzbar |
| barcode | python-barcode 生成 | python-barcode |
| text_to_image | PIL ImageDraw 文字渲染 + 自动换行 | Pillow |
| meme | PIL 顶部/底部描边文字叠加 | Pillow |
| similarity | imagehash 感知哈希(p/d/a/w hash) | imagehash |
| duplicate | 批量感知哈希 + 汉明距离分组 | imagehash |
| quality_score | Laplacian 方差 + 噪点估计 + 色彩丰富度 | OpenCV + numpy |
| color_picker | PIL getpixel 像素/区域颜色提取 | Pillow |
| batch_process | 5 种操作批处理 → zip | Pillow |
| batch_rename | 模板命名 + 序号 padding → zip | 标准库 |
| batch_resize | cover/contain/stretch 三模式 → zip | Pillow |
| preset_save | JSON 文件 CRUD | 标准库 json |

---

## 5. 前端架构

### 5.1 路由设计

所有路由集中定义在 `src/router/index.ts`：

```typescript
export const ROUTES = [
  {
    path: '/crop-rotate',
    name: 'CropRotate',
    component: () => import('@/views/CropRotate.vue'),
    meta: { title: '裁剪旋转', icon: 'Crop', category: 'basic' }
  },
  // ... 共 45 条
]
```

- `meta.icon` — Element Plus 图标名，侧边栏渲染
- `meta.category` — 分类键，侧边栏分组依据
- 默认路由重定向到 `/id-photo`

### 5.2 组件层级

```
App.vue
 └── MainLayout.vue (侧边栏 + 头部 + 内容区)
      └── <router-view>
           ├── ToolPage.vue           ← 约 35 个视图复用
           │    ├── ImageUploader     (拖拽/粘贴/点击上传)
           │    ├── [slot:params]     (各页面自定义参数)
           │    └── ImageCompare      (并排/滑动双模式对比)
           │
           └── 自定义视图             ← 约 10 个复杂页面自管状态
                ├── ImageUploader
                ├── ParamSlider
                └── ColorPicker
```

### 5.3 视图模式

**模式 A：ToolPage 包装**（35 个页面）
```vue
<template>
  <ToolPage module="compress" :params="params">
    <template #params>
      <el-slider v-model="params.quality" :min="1" :max="100" />
    </template>
  </ToolPage>
</template>
```
ToolPage 自动处理：上传 → 处理按钮 → 进度条 → 结果对比 → 下载。

**模式 B：独立实现**（10 个页面）
- 多文件上传（PhotoCollage, LongStitch, ToPdf, BatchProcess 等）
- 双图对比（Similarity, ChangeBg）
- JSON 表格展示（ImageInfo, ColorAnalysis, PresetSave）
- 特殊交互（IdPhoto, QrDecode, ColorPickerView）

### 5.4 设计系统

```css
--primary: #6C5CE7;          /* 紫色主色 */
--primary-light: #a29bfe;    /* 浅紫 */
--sidebar-bg: #0f172a;       /* 深蓝灰侧边栏 */
--sidebar-hover: #1e293b;    /* 侧边栏 hover */
--content-bg: #f8fafc;       /* 内容区极浅灰 */
--card-bg: #ffffff;          /* 卡片白色 */
--text-primary: #1e293b;     /* 主文字 */
--text-secondary: #64748b;   /* 次文字 */
--text-muted: #94a3b8;       /* 辅助文字 */
--border-color: #e2e8f0;     /* 边框 */
--radius: 14px;              /* 圆角 */
```

紫色通过 CSS 覆盖注入 Element Plus 的按钮、滑块、开关、复选框、进度条、单选按钮等组件。

---

## 6. 关键设计决策

| 决策 | 原因 |
|------|------|
| 无数据库 | 纯工具型应用无持久化需求，预设用 JSON 文件 |
| 单端点模式 | `POST /api/{module}/process` 统一接口，前端调用零学习成本 |
| 纯 Python 实现 | 零外部 API 依赖，完全离线可用 |
| rembg CPU 版 | 无需 GPU，抠图效果优于 OpenCV GrabCut |
| OpenCV Haar Cascade 替代 mediapipe | 避免 mediapipe 同名 PyPI 包冲突 |
| PIL 替代 cv2.imwrite 保存文件 | OpenCV 不支持中文路径 |
| CSS 变量主题 | 全局统一配色，一处修改全局生效 |
| ToolPage 组件复用 | 约 70% 页面通过 ToolPage 实现，减少重复代码 |
| 分类折叠侧边栏 | 45 个入口平铺不可用，10 类折叠导航 |

---

## 7. 已知局限

| 局限 | 说明 |
|------|------|
| 人脸检测精度 | OpenCV Haar Cascade 不如深度学习方案（MTCNN/RetinaFace） |
| 老照片修复 | CLAHE + 去噪效果有限，真实修复需 GAN 模型 |
| 抠图速度 | rembg CPU 推理单张 ~2-5 秒 |
| 超分辨率 | INTER_CUBIC 插值是简单放大，非 AI 超分 |
| 换装效果 | 仅 V 领模板合成，非真实换装 |
| 图片转SVG | 需 potrace/自定义矢量化算法，暂未实现 |
| 无认证机制 | 仅适用于本地/可信环境 |
| 无国际化 | 仅中文 UI |

---

## 8. 扩展指南

### 添加新功能模块

**后端**（3 步）：
1. 在 `routers/` 下创建 `new_module.py`，按模板实现 `/api/new-module/process`
2. 在 `main.py` 中 import 并加入 `routers` 列表
3. 如需新依赖：`uv add <package>`

**前端**（3 步）：
1. 在 `views/` 下创建 `NewModule.vue`（ToolPage 包装或独立实现）
2. 在 `router/index.ts` 的 `ROUTES` 中添加一条路由
3. 确保 `meta.category` 分配到正确的分类

### 添加新依赖需评估
- 是否纯 Python？（避免 C++ 编译依赖）
- 安装体积多大？（>100MB 需讨论）
- 是否需要 GPU？（CPU only 优先）
