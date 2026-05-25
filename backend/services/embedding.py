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
            import shutil
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            if not fpath.exists():
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
                f"模型文件缺失。需要 {onnx_path} 和 {tokenizer_path}"
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
