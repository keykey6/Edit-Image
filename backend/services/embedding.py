"""文本嵌入服务。使用 jieba 分词 + TF-IDF 做中文语义匹配。
无需下载模型，毫秒级响应，适合功能搜索场景。
"""
import logging
from collections import Counter
import math

import numpy as np

logger = logging.getLogger(__name__)

# 全局 TF-IDF 词表，由 build_vocabulary() 构建
_vocabulary: dict[str, int] = {}       # term -> index
_idf: dict[str, float] = {}            # term -> idf weight
_vocab_size: int = 0


def _tokenize(text: str) -> list[str]:
    """中文分词 + 字符级 bigram 增强。"""
    try:
        import jieba
        words = list(jieba.cut(text))
    except ImportError:
        words = list(text)

    terms = []
    for w in words:
        w = w.strip()
        if not w:
            continue
        terms.append(w)
        # 对中文词汇做字符 bigram 增强匹配
        if len(w) >= 2 and any('一' <= c <= '鿿' for c in w):
            for i in range(len(w) - 1):
                terms.append(w[i:i + 2])

    return terms


def build_vocabulary(documents: list[str]):
    """根据文档集合构建 TF-IDF 词表。"""
    global _vocabulary, _idf, _vocab_size

    doc_count = len(documents)
    doc_freq: Counter = Counter()

    all_terms: list[list[str]] = []
    for doc in documents:
        terms = _tokenize(doc)
        all_terms.append(terms)
        doc_freq.update(set(terms))

    # 构建词表（按词频排序，取前 3000 个）
    sorted_terms = sorted(doc_freq.items(), key=lambda x: -x[1])[:3000]
    _vocabulary = {term: idx for idx, (term, _) in enumerate(sorted_terms)}
    _vocab_size = len(_vocabulary)

    # 计算 IDF
    for term, idx in _vocabulary.items():
        df = doc_freq.get(term, 1)
        _idf[term] = math.log((doc_count + 1) / (df + 1)) + 1.0

    logger.info(f"TF-IDF 词表构建完毕，词数: {_vocab_size}")


def _encode_sparse(terms: list[str]) -> np.ndarray:
    """将分词结果编码为 TF-IDF 加权向量。"""
    tf: Counter = Counter()
    for t in terms:
        if t in _vocabulary:
            tf[t] += 1

    vec = np.zeros(_vocab_size, dtype=np.float32)
    if not tf:
        return vec

    # TF-IDF weighting
    total = sum(tf.values())
    for term, count in tf.items():
        idx = _vocabulary[term]
        vec[idx] = (count / total) * _idf.get(term, 1.0)

    # L2 normalize
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


def encode(text: str) -> np.ndarray:
    """编码文本为 TF-IDF 向量。"""
    if not _vocabulary:
        raise RuntimeError("词表未初始化，请先调用 build_vocabulary()")
    terms = _tokenize(text)
    return _encode_sparse(terms)


def similarity(a: np.ndarray, b: np.ndarray) -> float:
    """余弦相似度（向量已归一化时等价于点积）。"""
    return float(np.dot(a, b))
