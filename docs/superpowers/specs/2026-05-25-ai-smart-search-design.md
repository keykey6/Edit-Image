# AI智能搜索 — 设计文档

## 概述

在首页添加自然语言搜索功能。用户用中文描述需求（如"把照片背景去掉"），后端用文本嵌入模型做语义匹配，返回最相关的功能推荐卡片。

## 用户故事

- 用户打开首页 → 看到搜索框 → 输入"想把两张图拼一起" → 看到"拼图""长图拼接"等推荐 → 点击进入功能页
- 用户不确定功能叫什么 → 描述需求 → AI 找到对应工具

## 技术方案

**模型**：`all-MiniLM-L6-v2` ONNX 版本，~23MB。通过 `onnxruntime` 推理（rembg 已依赖此库）。

**预计算**：启动时将 45 个功能的富文本描述编码为向量，存内存。每次搜索只编码用户查询，余弦相似度排序，毫秒级返回。

## 新增文件

| 文件 | 用途 |
|------|------|
| `backend/services/tool_descriptions.py` | 45 个功能的搜索描述数据（标题 + 关键词 + 使用场景） |
| `backend/services/embedding.py` | 模型下载/加载、文本→向量编码、相似度计算 |
| `backend/routers/smart_search.py` | `/api/smart-search` 端点 |
| `frontend/src/views/HomePage.vue` | 首页搜索界面 |

## 修改文件

| 文件 | 改动 |
|------|------|
| `backend/main.py` | 注册 smart_search router |
| `backend/config.py` | 添加模型缓存路径配置 |
| `frontend/src/router/index.ts` | `/` 改为指向 HomePage；侧边栏加首页入口 |
| `frontend/src/layouts/MainLayout.vue` | 可选：当前在首页时隐藏 header 描述 |

## API 设计

```
POST /api/smart-search
Content-Type: application/json

Request:  { "query": "把照片背景去掉", "top_n": 5 }
Response: {
  "results": [
    {
      "path": "/remove-bg",
      "title": "AI抠图",
      "description": "智能识别主体，一键去除背景",
      "category": "人像美化",
      "icon": "Scissor",
      "score": 0.92
    },
    ...
  ]
}
```

## 首页布局

- **未搜索**：大标题"超级图像工具箱" + 副标题 + 搜索框 + 10 类快捷入口
- **搜索中**：搜索框 + 加载动画
- **有结果**：搜索框 + 最多 5 张结果卡片（图标、名称、描述、分类标签、匹配百分比）
- **无结果**：搜索框 + 空状态提示

## 依赖变更

- 新增：`tokenizers`（用于 BERT tokenization）
- 复用：`onnxruntime`（已被 rembg 依赖）、`numpy`

## 边界情况

- 模型首次启动自动下载到本地缓存目录
- 下载失败时搜索端点返回 503，前端提示"搜索服务初始化中，请稍后重试"
- 空查询返回 400
- 查询超 200 字截断
