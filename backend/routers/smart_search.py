"""智能搜索 API。用户用自然语言描述需求，返回最匹配的功能推荐。"""
import logging

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
