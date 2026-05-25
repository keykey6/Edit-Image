# AI智能搜索 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在首页用自然语言描述需求，后端用 ONNX 文本嵌入模型做语义匹配，返回最相关的功能推荐。

**Architecture:** 后端启动时预计算 45 个功能描述向量存内存。用户搜索时编码查询向量，余弦相似度排序返回 Top-N。前端首页大搜索框 + 卡片式结果。

**Tech Stack:** FastAPI (后端), ONNX Runtime + tokenizers (嵌入模型), Vue3 + Element Plus (前端)

**Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` ONNX 版本，384维向量，支持中文。

---

### Task 1: 添加后端依赖

**Files:**
- Modify: `backend/pyproject.toml`

- [ ] **Step 1: 添加 tokenizers 和 huggingface_hub**

在 `pyproject.toml` 的 dependencies 列表末尾加入：

```toml
"tokenizers>=0.22.0",
"huggingface-hub>=0.30.0",
```

- [ ] **Step 2: 安装依赖**

```bash
cd backend && uv sync
```

Expected: 安装 tokenizers、huggingface-hub 及其子依赖，无报错。

- [ ] **Step 3: 验证**

```bash
cd backend && uv run python -c "from tokenizers import Tokenizer; from huggingface_hub import hf_hub_download; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
cd "c:/Users/董哲/Desktop/图片/super-image-toolbox"
git add backend/pyproject.toml backend/uv.lock
git commit -m "chore: add tokenizers and huggingface-hub for AI search embedding"
```

---

### Task 2: 创建功能搜索描述数据

**Files:**
- Create: `backend/services/tool_descriptions.py`

每一行是一个功能：`(path, title, icon, category_key, search_text)`。`search_text` 是用于语义匹配的富文本，包含功能名、关键词、使用场景、同义词。

- [ ] **Step 1: 创建 tool_descriptions.py**

```python
"""45 个功能的搜索描述数据。每项: (path, title, icon, category_key, search_text)
search_text 用于语义匹配，包含功能名、关键词、使用场景。
"""

TOOLS: list[tuple[str, str, str, str, str]] = [
    # ===== 图片调整 =====
    ("/crop-rotate", "裁剪旋转", "Crop", "basic",
     "裁剪旋转 裁切图片 旋转方向 翻转镜像 按比例裁剪 自由裁剪 任意角度旋转 纠正照片方向"),
    ("/compress", "图片压缩", "FolderOpened", "basic",
     "图片压缩 减小文件体积 缩小照片大小 压缩到指定大小 调整画质 JPEG压缩 PNG压缩 WebP压缩 批量压缩"),
    ("/format-convert", "格式转换", "Switch", "basic",
     "格式转换 图片格式互转 JPG转PNG PNG转JPG WebP转换 BMP转换 批量转换格式 改变图片类型"),
    ("/rounded-border", "圆角边框", "FullScreen", "basic",
     "圆角边框 圆角图片 给图片加边框 圆角矩形 四角圆角 自定义圆角大小 白色边框"),
    ("/image-info", "图片信息", "InfoFilled", "basic",
     "图片信息 查看图片属性 分辨率尺寸 文件大小 EXIF信息 拍摄参数 相机型号 GPS位置信息"),
    ("/dpi", "DPI设置", "ScaleToOriginal", "basic",
     "DPI设置 修改DPI 打印分辨率 300dpi 72dpi 修改分辨率 图片清晰度 打印图片"),

    # ===== 颜色与光影 =====
    ("/color-filter", "调色滤镜", "MagicStick", "color",
     "调色滤镜 滤镜效果 黑白滤镜 复古滤镜 暖色调 冷色调 日系色调 电影色调 色彩调节 照片调色 美化图片颜色"),
    ("/curve", "曲线调色", "TrendCharts", "color",
     "曲线调色 曲线工具 调整明暗 对比度调整 RGB曲线 色调曲线 专业调色 亮度对比度 高光阴影调整"),
    ("/hsl", "HSL调色", "Coin", "color",
     "HSL调色 色相饱和度 明度调整 改变色调 增加饱和度 降低亮度 色彩微调 颜色调整"),
    ("/dehaze", "去雾提亮", "Sunny", "color",
     "去雾提亮 去雾霾 照片去灰 增加对比度 雾天照片处理 清晰化 通透感 照片去朦胧"),
    ("/histogram", "图片直方图", "Histogram", "color",
     "图片直方图 查看直方图 曝光分析 RGB直方图 亮度分布 色彩分布 通道直方图 判断过曝欠曝"),
    ("/color-analysis", "色彩分析", "DataAnalysis", "color",
     "色彩分析 提取主色调 配色分析 颜色统计 调色板 色板提取 分析图片颜色 主题色识别"),

    # ===== 艺术效果 =====
    ("/sketch-effect", "素描漫画", "Brush", "effects",
     "素描漫画 照片变素描 铅笔素描 漫画效果 卡通化 手绘风格 线稿效果 艺术化 照片转手绘"),
    ("/shadow", "阴影倒影", "PictureFilled", "effects",
     "阴影倒影 添加阴影 倒影效果 镜面倒影 立体阴影 产品展示 图片立体感 投影"),
    ("/perspective", "透视矫正", "Crop", "effects",
     "透视矫正 梯形校正 文档扫描矫正 图片拉直 变形校正 建筑摄影矫正 手机拍文档"),

    # ===== 人像美化 =====
    ("/id-photo", "证件照", "Camera", "portrait",
     "证件照 一寸照片 二寸照片 护照照片 签证照片 换底色 证件照制作 照片尺寸 标准证件照 免冠照片"),
    ("/remove-bg", "AI抠图", "Scissor", "portrait",
     "AI抠图 去除背景 背景消除 智能抠图 一键去背景 人物抠图 商品抠图 透明背景 把背景去掉 去掉背景"),
    ("/change-bg", "换背景", "Picture", "portrait",
     "换背景 更换背景 替换背景 照片换底 白色背景 蓝色背景 自定义背景 证件照换底色"),
    ("/face-beauty", "人像美颜", "Star", "portrait",
     "人像美颜 美颜 磨皮美白 瘦脸 自拍美化 皮肤美白 人像美容 脸部修饰 祛痘 光滑皮肤"),
    ("/photo-restore", "老照片修复", "Timer", "portrait",
     "老照片修复 照片修复 去除划痕 旧照片翻新 去噪点 增强清晰度 修复破损照片 老照片上色 黑白照片修复"),
    ("/suit-change", "证件照换装", "User", "portrait",
     "证件照换装 换西装 换正装 证件照衣服 换职业装 西装证件照 正装照 换衣服"),

    # ===== 安全与隐私 =====
    ("/watermark-add", "水印添加", "Edit", "privacy",
     "水印添加 加水印 图片水印 文字水印 图片水印 版权保护 防盗图 签名水印 批量加水印"),
    ("/watermark-remove", "水印去除", "Delete", "privacy",
     "水印去除 去水印 消除水印 删除水印 移除水印 去除LOGO 去掉水印 除水印"),
    ("/blur-mosaic", "模糊打码", "Hide", "privacy",
     "模糊打码 马赛克 打码 模糊人脸 遮挡敏感信息 车牌打码 高斯模糊 身份信息打码 隐私保护"),
    ("/privacy-erase", "隐私擦除", "RemoveFilled", "privacy",
     "隐私擦除 删除EXIF 清除图片信息 去除拍摄数据 隐私保护 抹除GPS位置 清除相机信息"),
    ("/encrypt", "图片加密", "Lock", "privacy",
     "图片加密 照片加密 密码保护 隐私照片 文件加密 AES加密 图片加锁 加密图片"),

    # ===== 拼接与布局 =====
    ("/photo-collage", "拼图", "Grid", "layout",
     "拼图 照片拼接 图片拼接 多图合成 拼图模板 网格拼图 组合图片 把多张拼一起"),
    ("/grid-split", "切图", "Operation", "layout",
     "切图 图片切割 九宫格 均匀分割 切分成多张 图片切片 均分图片 大图切小图"),
    ("/long-stitch", "长图拼接", "Connection", "layout",
     "长图拼接 长截图 聊天记录拼接 多张图拼成一张 纵向拼接 横向拼接 长图制作 滚动截图拼接"),
    ("/social-media", "社交媒体配图", "Share", "layout",
     "社交媒体配图 朋友圈裁剪 封面图 头像裁剪 各平台尺寸 小红书配图 抖音封面 社交网络图片裁剪"),

    # ===== 格式转换 =====
    ("/super-res", "分辨率放大", "ZoomIn", "convert",
     "分辨率放大 提高分辨率 图片放大 增加像素 放大清晰度 图片无损放大 超分辨率 图片变清晰"),
    ("/to-pdf", "图片转PDF", "Document", "convert",
     "图片转PDF 图片合并PDF 多图转一个PDF PDF导出 图片转文档 生成PDF文件 照片转PDF"),
    ("/to-ico", "图片转ICO", "StarFilled", "convert",
     "图片转ICO 制作图标 网站图标 应用图标 图标制作 favicon 小图标 多尺寸图标"),

    # ===== 生成与识别 =====
    ("/qrcode-gen", "二维码生成", "Postcard", "generate",
     "二维码生成 制作二维码 生成二维码 URL二维码 文本二维码 WiFi二维码 收款码 名片二维码"),
    ("/qr-decode", "二维码解码", "View", "generate",
     "二维码解码 识别二维码 扫描二维码 读取二维码内容 解析二维码 扫码 翻译二维码"),
    ("/barcode", "条形码生成", "Barcode", "generate",
     "条形码生成 条形码 商品条码 ISBN条码 条码制作 生成条码 商品编码"),
    ("/text-to-image", "文字转图片", "EditPen", "generate",
     "文字转图片 文本生成图片 文字排版 生成文字海报 长文截图 文字卡片 名言卡片 文字图片化"),
    ("/meme", "表情包制作", "Smile", "generate",
     "表情包制作 搞笑图片 配文字表情包 做表情包 梗图 表情包DIY 给图片加搞笑文字 制作表情"),

    # ===== 智能分析 =====
    ("/similarity", "相似度对比", "Link", "analysis",
     "相似度对比 图片相似度 比较两张图 找不同 对比差异 图片比对 两张图是否相同 图片查重"),
    ("/duplicate", "重复检测", "CopyDocument", "analysis",
     "重复检测 查找重复图片 批量查重 相似图片查找 找出重复 去重 找相同图片 清除重复照片"),
    ("/quality-score", "质量评分", "Medal", "analysis",
     "质量评分 图片质量 清晰度评分 画质评分 照片质量评估 模糊检测 噪点评分 图片好坏评分"),
    ("/color-picker", "取色器", "ColorPicker", "analysis",
     "取色器 颜色提取 取色 吸管工具 像素颜色 区域颜色 获取颜色值 HEX RGB 色号"),

    # ===== 批量与预设 =====
    ("/batch-process", "批量处理", "List", "batch",
     "批量处理 批量编辑 批量调色 批量滤镜 批量加水印 批量裁切 一键处理多张 自动化处理"),
    ("/batch-rename", "批量重命名", "Sort", "batch",
     "批量重命名 批量改名 重命名照片 序号命名 日期命名 文件批量改名 统一命名 批量文件重命名"),
    ("/batch-resize", "BatchResize", "Odometer", "batch",
     "批量改尺寸 批量调整大小 统一尺寸 批量缩放 批量改分辨率 批量缩小 等比缩放多张图片"),
    ("/preset-save", "处理预设", "Collection", "batch",
     "处理预设 预设管理 保存处理方案 快捷处理 收藏操作 常用操作 方案复用 一键套用预设"),
]

# 分类名映射（用于前端展示）
CATEGORY_NAMES: dict[str, str] = {
    "basic": "图片调整",
    "color": "颜色与光影",
    "effects": "艺术效果",
    "portrait": "人像美化",
    "privacy": "安全与隐私",
    "layout": "拼接与布局",
    "convert": "格式工具",
    "generate": "生成与识别",
    "analysis": "智能分析",
    "batch": "批量操作",
}
```

- [ ] **Step 2: Commit**

```bash
git add backend/services/tool_descriptions.py
git commit -m "feat: add tool search descriptions for AI semantic search"
```

---

### Task 3: 创建嵌入模型服务

**Files:**
- Create: `backend/services/embedding.py`

处理 ONNX 模型下载、加载、文本编码、相似度计算。启动时下载模型（按需），加载到内存。

- [ ] **Step 1: 创建 embedding.py**

```python
"""文本嵌入服务。使用 paraphrase-multilingual-MiniLM-L12-v2 ONNX 模型做语义编码。"""
import os
import logging
from pathlib import Path
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer

logger = logging.getLogger(__name__)

MODEL_REPO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_FILES = ["model.onnx", "tokenizer.json"]
EMBEDDING_DIM = 384
MAX_SEQ_LEN = 128

# 模型缓存路径：优先环境变量，否则 ~/.cache/image-toolbox/models/
DEFAULT_CACHE = Path.home() / ".cache" / "image-toolbox" / "models"


def _ensure_model_files() -> Path:
    """确保模型文件存在。从 HuggingFace 下载或使用本地缓存。"""
    cache_dir = Path(os.environ.get("MODEL_CACHE_DIR", str(DEFAULT_CACHE)))
    cache_dir.mkdir(parents=True, exist_ok=True)

    repo_hash = MODEL_REPO.replace("/", "--")
    model_dir = cache_dir / repo_hash

    for fname in MODEL_FILES:
        fpath = model_dir / fname
        if not fpath.exists():
            logger.info(f"下载模型文件: {fname}")
            downloaded = hf_hub_download(
                repo_id=MODEL_REPO,
                filename=f"onnx/{fname}",
                cache_dir=str(model_dir.parent),
            )
            # huggingface_hub 会缓存到嵌套目录，复制到扁平目录
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            if not fpath.exists():
                import shutil
                shutil.copy2(downloaded, fpath)

    return model_dir


class EmbeddingService:
    """文本嵌入服务：编码文本为向量，计算相似度。"""

    def __init__(self):
        self.session: ort.InferenceSession | None = None
        self.tokenizer: Tokenizer | None = None

    def initialize(self):
        """加载模型和分词器。首次运行会下载模型文件。"""
        model_dir = _ensure_model_files()
        onnx_path = model_dir / "model.onnx"
        tokenizer_path = model_dir / "tokenizer.json"

        if not onnx_path.exists() or not tokenizer_path.exists():
            raise FileNotFoundError(
                f"模型文件缺失。from {onnx_path} to exist in {model_dir}"
            )

        self.session = ort.InferenceSession(
            str(onnx_path),
            providers=["CPUExecutionProvider"],
        )
        self.tokenizer = Tokenizer.from_file(str(tokenizer_path))
        logger.info("嵌入模型加载完毕")

    def encode(self, text: str) -> np.ndarray:
        """编码文本为归一化嵌入向量 (384,)。"""
        if not self.session or not self.tokenizer:
            raise RuntimeError("模型未初始化")

        encoded = self.tokenizer.encode(text)
        ids = encoded.ids[:MAX_SEQ_LEN]
        seq_len = len(ids)

        # BERT 标准 tokenizer 没有 pad_token，使用 0
        input_ids = np.zeros((1, MAX_SEQ_LEN), dtype=np.int64)
        attention_mask = np.zeros((1, MAX_SEQ_LEN), dtype=np.int64)
        token_type_ids = np.zeros((1, MAX_SEQ_LEN), dtype=np.int64)

        input_ids[0, :seq_len] = ids
        attention_mask[0, :seq_len] = 1

        outputs = self.session.run(
            None,
            {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "token_type_ids": token_type_ids,
            },
        )
        # outputs[0] = last_hidden_state (1, seq_len, 384)
        # Mean pooling over token dimension
        hidden = outputs[0][0]                    # (seq_len, 384)
        mask = attention_mask[0][:, None]          # (seq_len, 1)
        masked = hidden * mask
        summed = masked.sum(axis=0)                # (384,)
        count = mask.sum()
        embedding = summed / max(count, 1)        # (384,)

        # L2 normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding.astype(np.float32)

    def similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """余弦相似度（向量已归一化时等价于点积）。"""
        return float(np.dot(a, b))


# 全局单例
_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
        _embedding_service.initialize()
    return _embedding_service
```

- [ ] **Step 2: 验证后端能加载模型（需网络）**

```bash
cd backend && uv run python -c "
from services.embedding import get_embedding_service
svc = get_embedding_service()
v = svc.encode('去除图片背景')
print(f'vector shape: {v.shape}, norm: {(v**2).sum():.3f}')
"
```

Expected: `vector shape: (384,), norm: 0.999` (或接近1.0)

- [ ] **Step 3: Commit**

```bash
git add backend/services/embedding.py
git commit -m "feat: add ONNX text embedding service for semantic search"
```

---

### Task 4: 创建智能搜索 API 端点

**Files:**
- Create: `backend/routers/smart_search.py`

在启动时预计算 45 个工具向量的端点。

- [ ] **Step 1: 创建 smart_search.py**

```python
"""智能搜索 API。用户用自然语言描述需求，返回最匹配的功能推荐。"""
import logging
from contextlib import asynccontextmanager

import numpy as np
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.tool_descriptions import TOOLS, CATEGORY_NAMES
from services.embedding import get_embedding_service, EmbeddingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/smart-search", tags=["智能搜索"])

# 预计算存储：工具向量 + 工具元数据
_tool_embeddings: np.ndarray | None = None
_tool_metas: list[dict] = []
_search_ready: bool = False


def _build_tool_index(service: EmbeddingService):
    """为 45 个工具预计算向量索引。"""
    global _tool_embeddings, _tool_metas, _search_ready

    embeddings = []
    metas = []
    for path, title, icon, cat_key, search_text in TOOLS:
        vec = service.encode(search_text)
        embeddings.append(vec)
        metas.append({
            "path": path,
            "title": title,
            "icon": icon,
            "category": CATEGORY_NAMES.get(cat_key, cat_key),
            "description": search_text.split(" ")[0] if search_text else title,
        })

    _tool_embeddings = np.stack(embeddings, axis=0)  # (45, 384)
    _tool_metas = metas
    _search_ready = True
    logger.info(f"工具索引构建完毕，共 {len(metas)} 个功能")


@router.on_event("startup")
def _on_startup():
    """应用启动时构建索引。失败则标记未就绪。"""
    try:
        svc = get_embedding_service()
        _build_tool_index(svc)
    except Exception as e:
        logger.error(f"智能搜索索引构建失败: {e}")
        _search_ready = False


@router.get("/health")
async def health():
    """查询搜索服务是否就绪。"""
    return {"ready": _search_ready}


@router.post("")
async def smart_search(request: Request):
    """搜索匹配的工具。"""
    if not _search_ready or _tool_embeddings is None:
        return JSONResponse(
            {"detail": "搜索服务正在初始化，请稍后重试", "results": []},
            status_code=503,
        )

    body = await request.json()
    query = (body.get("query") or "").strip()
    top_n = min(body.get("top_n", 5), 10)

    if not query:
        return JSONResponse(
            {"detail": "请输入搜索内容", "results": []},
            status_code=400,
        )

    if len(query) > 200:
        query = query[:200]

    # 编码查询
    svc = get_embedding_service()
    query_vec = svc.encode(query)  # (384,)

    # 余弦相似度 = 归一化向量点积
    scores = np.dot(_tool_embeddings, query_vec)  # (45,)

    # 排序取 Top-N
    top_indices = np.argsort(scores)[::-1][:top_n]

    results = []
    for idx in top_indices:
        score = float(scores[idx])
        if score < 0.2:    # 相关性太低，截断
            break
        meta = _tool_metas[idx].copy()
        meta["score"] = round(score, 4)
        results.append(meta)

    return {"results": results}
```

- [ ] **Step 2: Commit**

```bash
git add backend/routers/smart_search.py
git commit -m "feat: add smart search API endpoint with vector similarity"
```

---

### Task 5: 注册路由

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 1: 在 main.py 注册 smart_search 路由**

在 [backend/main.py](backend/main.py) ：

找到 `from routers.preset_save import router as preset_save` 这行（第 49 行），在后面加：

```python
from routers.smart_search import router as smart_search
```

找到 `routers = [` 列表末尾（`preset_save` 之后），加：

```python
    smart_search,
```

即把 `smart_search` 加入 `routers` 列表。

- [ ] **Step 2: Commit**

```bash
git add backend/main.py
git commit -m "feat: register smart-search router"
```

---

### Task 6: 添加前端 API 函数

**Files:**
- Modify: `frontend/src/api/index.ts`

- [ ] **Step 1: 添加 smartSearch 函数和相关类型**

在 [frontend/src/api/index.ts](frontend/src/api/index.ts) 文件末尾追加：

```typescript
export interface SearchResult {
  path: string
  title: string
  description: string
  category: string
  icon: string
  score: number
}

export interface SearchResponse {
  results: SearchResult[]
  detail?: string
}

export async function smartSearch(query: string, topN = 5): Promise<SearchResponse> {
  const res = await api.post('/smart-search', { query, top_n: topN })
  return res.data
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/api/index.ts
git commit -m "feat: add smartSearch API function to frontend"
```

---

### Task 7: 创建首页搜索界面

**Files:**
- Create: `frontend/src/views/HomePage.vue`

- [ ] **Step 1: 创建 HomePage.vue**

```vue
<template>
  <div class="home-page">
    <!-- Hero -->
    <div class="hero">
      <div class="hero-icon">
        <el-icon :size="48"><PictureFilled /></el-icon>
      </div>
      <h1 class="hero-title">超级图像工具箱</h1>
      <p class="hero-subtitle">45个工具，一个搜索框找到你想要的</p>
    </div>

    <!-- Search -->
    <div class="search-section">
      <el-input
        v-model="query"
        size="large"
        placeholder="描述你想做什么，比如"把背景去掉"、"压缩图片大小"..."
        clearable
        @input="onInput"
        @clear="onClear"
        @keydown.enter="doSearch"
      >
        <template #prefix>
          <el-icon :size="20"><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- Loading -->
    <div v-if="searching" class="status-text">搜索中...</div>

    <!-- Results -->
    <div v-else-if="results.length > 0" class="results-grid">
      <div
        v-for="item in results"
        :key="item.path"
        class="result-card"
        @click="goTo(item.path)"
      >
        <div class="card-top">
          <el-icon :size="22"><component :is="item.icon" /></el-icon>
          <span class="card-title">{{ item.title }}</span>
          <span class="card-score">{{ Math.round(item.score * 100) }}%</span>
        </div>
        <p class="card-desc">{{ item.description }}</p>
        <el-tag size="small" type="info">{{ item.category }}</el-tag>
      </div>
    </div>

    <!-- No results -->
    <div v-else-if="searched && !searching" class="status-text empty">
      <el-icon :size="36"><Search /></el-icon>
      <p>没有匹配的功能，试试其他描述</p>
    </div>

    <!-- Categories -->
    <div v-if="!searched && !searching" class="categories-section">
      <h3 class="section-title">按分类浏览</h3>
      <div class="category-tags">
        <span
          v-for="(label, key) in CATEGORY_NAMES"
          :key="key"
          class="category-tag"
          @click="searchCategory(label)"
        >{{ label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search, PictureFilled } from '@element-plus/icons-vue'
import { smartSearch, type SearchResult } from '@/api'
import { CATEGORIES } from '@/router'

// 图标已全局注册（见 main.ts），直接使用 component :is="item.icon"
const CATEGORY_NAMES = CATEGORIES

const router = useRouter()
const query = ref('')
const results = ref<SearchResult[]>([])
const searching = ref(false)
const searched = ref(false)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

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
  router.push(path)
}
</script>

<style scoped>
.home-page {
  max-width: 720px;
  margin: 0 auto;
  padding: 60px 20px;
}

/* Hero */
.hero { text-align: center; margin-bottom: 32px; }
.hero-icon {
  width: 80px; height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #6C5CE7, #a29bfe);
  border-radius: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.hero-title { font-size: 28px; font-weight: 800; color: var(--text-primary); margin: 0 0 8px; }
.hero-subtitle { font-size: 15px; color: var(--text-muted); margin: 0; }

/* Search */
.search-section { margin-bottom: 28px; }
.search-section :deep(.el-input__wrapper) {
  border-radius: 14px;
  padding: 6px 16px;
  box-shadow: 0 2px 12px rgba(108, 92, 231, 0.1);
}

/* Status */
.status-text { text-align: center; color: var(--text-muted); padding: 40px 0; }
.status-text.empty { color: var(--text-muted); }
.status-text.empty p { margin-top: 12px; }

/* Results */
.results-grid { display: flex; flex-direction: column; gap: 10px; }
.result-card {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px 20px;
  cursor: pointer;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.result-card:hover {
  border-color: var(--primary-light);
  box-shadow: 0 4px 16px rgba(108, 92, 231, 0.12);
}
.card-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}
.card-title { font-size: 15px; font-weight: 600; color: var(--text-primary); }
.card-score {
  margin-left: auto;
  font-size: 12px;
  color: var(--primary);
  font-weight: 600;
}
.card-desc { font-size: 13px; color: var(--text-secondary); margin: 0 0 8px; }

/* Categories */
.categories-section { margin-top: 48px; }
.section-title { font-size: 14px; color: var(--text-muted); margin: 0 0 14px; text-align: center; }
.category-tags { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
.category-tag {
  padding: 8px 20px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 22px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}
.category-tag:hover {
  border-color: var(--primary-light);
  color: var(--primary);
  background: rgba(108, 92, 231, 0.04);
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/HomePage.vue
git commit -m "feat: add HomePage with AI search interface"
```

---

### Task 8: 更新路由配置

**Files:**
- Modify: `frontend/src/router/index.ts`

- [ ] **Step 1: 将首页路由指向 HomePage，保留侧边栏入口**

在 [frontend/src/router/index.ts](frontend/src/router/index.ts) 做以下改动：

1. 在文件顶部 import 区域，其他 import 之后加入：

```typescript
import HomePage from '@/views/HomePage.vue'
```

2. 找到 `{ path: '/', redirect: '/id-photo' },` 这一行，改为：

```typescript
    { path: '/', name: 'Home', component: HomePage, meta: { title: '首页', icon: 'HomeFilled', category: '' } },
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/router/index.ts
git commit -m "feat: route / to new HomePage with AI search"
```

---

### Task 9: 更新侧边栏布局

**Files:**
- Modify: `frontend/src/layouts/MainLayout.vue`

在侧边栏最顶部（logo 下方、分类导航上方）添加首页入口。

- [ ] **Step 1: 在侧边栏导航区域加首页入口**

找到文件 `frontend/src/layouts/MainLayout.vue`，在 `<nav class="sidebar-nav">` 和第一个 `<div v-for="cat in categories"` 之间，添加：

```vue
        <router-link to="/" class="nav-item nav-home" active-class="nav-active" exact-active-class="nav-active">
          <el-icon :size="16"><HomeFilled /></el-icon>
          <span>首页</span>
        </router-link>
```

同时在 `<script setup>` 的 import 中，找到 element-plus icons 的导入（如果有的话），确保 `HomeFilled` 可用。当前代码没有直接 import 图标组件，因为图标是通过 `component :is` 动态渲染的。需要在 script 中 import：

```typescript
import { HomeFilled } from '@element-plus/icons-vue'
```

> 注意：当前 MainLayout 使用 `component :is="item.icon"` 动态渲染，但首页入口是固定的静态链接，需要确保 `HomeFilled` 在模板中可用。最简单的方式：在 `<script setup>` 中 import `HomeFilled`。

- [ ] **Step 2: Commit**

```bash
git add frontend/src/layouts/MainLayout.vue
git commit -m "feat: add home entry to sidebar navigation"
```

---

### Task 10: 端到端验证

- [ ] **Step 1: 启动后端并验证 API**

```bash
cd backend && uv run uvicorn main:app --host 0.0.0.0 --port 9000 &
sleep 10
# 检查搜索服务就绪
curl -s http://localhost:9000/api/smart-search/health
# Expected: {"ready":true}

# 测试搜索
curl -s -X POST http://localhost:9000/api/smart-search \
  -H "Content-Type: application/json" \
  -d '{"query":"把照片背景去掉","top_n":3}'
# Expected: JSON results 数组，第一个应该是"AI抠图"
```

- [ ] **Step 2: 启动前端并手动测试**

```bash
cd frontend && pnpm dev
# 浏览器打开 http://localhost:5173
# 应该在首页看到搜索框
# 输入"把背景去掉"，应该看到AI抠图、换背景等卡片
# 点击卡片应跳转到对应功能页
```

- [ ] **Step 3: 检查回归**

- 侧边栏仍然正常显示所有 45 个功能
- 直接访问 `/id-photo` 等路径仍然正常工作
- 从搜索结果跳转到功能页后，功能正常使用

- [ ] **Step 4: Commit 验证记录（如有修改）**

```bash
git status
# 如有修改，提交
```

---

### Task 11: 构建生产版本验证

- [ ] **Step 1: 构建前端**

```bash
cd frontend && pnpm build
```

Expected: 类型检查通过，构建成功，`dist/` 目录生成。

- [ ] **Step 2: 构建后确认 dist 结构**

```bash
ls frontend/dist/
```

Expected: `index.html`, `assets/` 目录存在。
