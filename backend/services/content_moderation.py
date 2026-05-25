"""内容安全审核服务。基于 OpenCV 多阶段启发式检测，
对上传图片进行 NSFW/暴力/违规内容拦截。纯本地运行，无云 API 依赖。

检测策略：
  阶段 0 — 人脸检测（毫秒级）
    检测到人脸 → 判定为正常肖像，直接放行，不再检查肤色。
  阶段 1 — 肤色多区域分析（毫秒级）
    肤色区域数 ≥ 3 且均较大 → NSFW 嫌疑（正常肖像仅 1-2 个肤色区）。
  阶段 2 — 血腥红色分析（毫秒级）
    大面积连续暗红色 → 暴力嫌疑。
"""

import logging
import os
import shutil
import tempfile
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# ============================================================
# 可调阈值
# ============================================================
FACE_MIN_SIZE = (40, 40)       # 最小人脸尺寸（像素）
SKIN_REGION_COUNT_BLOCK = 3    # 显著肤色区域 ≥ N 个判定可疑
SKIN_REGION_MIN_AREA = 0.03    # 每个肤色区域至少占画面 3% 才算"显著"
BLOOD_RATIO_BLOCK = 0.12       # 红色区域占比超过此值触发
BLOOD_SATURATION_MIN = 80      # 血腥红色最低饱和度
BLOOD_VALUE_MAX = 180          # 血腥红色最高亮度（深红色更可疑）
BLOOD_CONTIGUITY_MIN = 0.25    # 红色区域最大连通域占比下限


@dataclass
class ModerationResult:
    passed: bool
    reason: str = ""
    faces: int = 0
    skin_ratio: float = 0.0
    skin_regions: int = 0
    blood_ratio: float = 0.0
    blood_contiguity: float = 0.0


# 懒加载人脸检测器
_face_cascade: cv2.CascadeClassifier | None = None
_cascade_loaded: bool = False  # 是否已尝试加载（避免反复重试）


def _get_face_cascade() -> cv2.CascadeClassifier | None:
    """获取人脸检测器。OpenCV C++ 无法读取中文路径，需复制到临时目录。"""
    global _face_cascade, _cascade_loaded
    if _cascade_loaded:
        return _face_cascade

    _cascade_loaded = True

    src = cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
    if not os.path.exists(src):
        # 尝试其他文件名
        for name in ["haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt.xml"]:
            candidate = cv2.data.haarcascades + name
            if os.path.exists(candidate):
                src = candidate
                break
        else:
            logger.warning("找不到人脸检测模型文件")
            return None

    try:
        # 复制到无中文的临时目录以规避 OpenCV C++ 路径问题
        tmp_dir = tempfile.gettempdir()
        dst = os.path.join(tmp_dir, "haarcascade_face.xml")
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        _face_cascade = cv2.CascadeClassifier(dst)
        if _face_cascade.empty():
            logger.warning("人脸检测模型加载失败")
            _face_cascade = None
        else:
            logger.info("人脸检测模型加载成功")
    except Exception as e:
        logger.warning(f"人脸检测模型加载异常: {e}")
        _face_cascade = None

    return _face_cascade


def _detect_faces(gray: np.ndarray) -> int:
    """检测灰度图中的人脸数量。返回 0 表示未检测到或检测器不可用。"""
    cascade = _get_face_cascade()
    if cascade is None:
        return 0
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=FACE_MIN_SIZE,
    )
    return len(faces)


def _skin_mask(img_bgr: np.ndarray) -> np.ndarray:
    """YCrCb 肤色掩码。"""
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    return cv2.inRange(ycrcb, lower, upper)


def _skin_region_count(mask: np.ndarray, total_pixels: int) -> int:
    """统计有多少个'显著'肤色连通区域。

    正常肖像通常只有 1-2 个（面部 + 颈部/手部），
    NSFW 内容通常有多个分散的大面积肤色区域。
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = total_pixels * SKIN_REGION_MIN_AREA
    significant = sum(1 for c in contours if cv2.contourArea(c) >= min_area)
    return significant


def _blood_mask(img_bgr: np.ndarray) -> np.ndarray:
    """HSV 血腥红色掩码——高饱和、偏低亮度的红色区域。"""
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower_r1 = np.array([0, BLOOD_SATURATION_MIN, 30], dtype=np.uint8)
    upper_r1 = np.array([10, 255, BLOOD_VALUE_MAX], dtype=np.uint8)
    lower_r2 = np.array([170, BLOOD_SATURATION_MIN, 30], dtype=np.uint8)
    upper_r2 = np.array([180, 255, BLOOD_VALUE_MAX], dtype=np.uint8)
    m1 = cv2.inRange(hsv, lower_r1, upper_r1)
    m2 = cv2.inRange(hsv, lower_r2, upper_r2)
    return cv2.bitwise_or(m1, m2)


def _max_contour_ratio(mask: np.ndarray) -> float:
    """掩码中最大连通域占总面积的比例。"""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 0.0
    largest = max(cv2.contourArea(c) for c in contours)
    total = mask.shape[0] * mask.shape[1]
    return largest / total if total > 0 else 0.0


def moderate(filepath: str) -> ModerationResult:
    """对图片文件进行内容安全审核。

    返回 ModerationResult，passed=True 表示审核通过。
    """
    # 使用 PIL 读取以规避 OpenCV 在 Windows 上的中文路径问题，
    # 然后转为 OpenCV 格式（BGR numpy array）进行后续处理
    try:
        pil_img = Image.open(filepath).convert("RGB")
        img = np.array(pil_img, dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logger.warning(f"无法读取图片用于审核: {filepath} — {e}")
        return ModerationResult(passed=False, reason="无法读取图片文件，请确认文件格式正确")

    h, w = img.shape[:2]
    total_pixels = h * w

    # ---- 阶段 0：人脸检测 ----
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    num_faces = _detect_faces(gray)

    if num_faces > 0:
        logger.debug(f"审核通过 — 检测到 {num_faces} 张人脸，判定为正常肖像")
        return ModerationResult(passed=True, faces=num_faces)

    # ---- 阶段 1：肤色多区域分析 ----
    skin = _skin_mask(img)
    skin_ratio = float(np.count_nonzero(skin) / total_pixels)
    skin_regions = _skin_region_count(skin, total_pixels)

    # ---- 阶段 2：血腥红色分析 ----
    blood = _blood_mask(img)
    blood_ratio = float(np.count_nonzero(blood) / total_pixels)
    blood_contiguity = _max_contour_ratio(blood)

    logger.debug(
        f"内容审核 — 人脸:{num_faces} 肤色:{skin_ratio:.3f} "
        f"肤色区:{skin_regions} 红色:{blood_ratio:.3f} 红色连通:{blood_contiguity:.3f}"
    )

    # 肤色区域数 ≥ 阈值 → NSFW 嫌疑
    # 正常人像（无检测到人脸的情况）：面部 + 脖颈最多 2 个显著区域
    # NSFW：多个分散的大面积肤色区
    if skin_regions >= SKIN_REGION_COUNT_BLOCK:
        logger.info(
            f"审核拦截 — 肤色区域过多 ({skin_regions} 个，占比 {skin_ratio:.2%})"
        )
        return ModerationResult(
            passed=False,
            reason="检测到图片可能包含不适宜内容，已被安全策略拦截。如有误判请联系管理员。",
            faces=num_faces,
            skin_ratio=skin_ratio,
            skin_regions=skin_regions,
            blood_ratio=blood_ratio,
            blood_contiguity=blood_contiguity,
        )

    # 血腥红色 → 暴力嫌疑
    if blood_ratio > BLOOD_RATIO_BLOCK and blood_contiguity > BLOOD_CONTIGUITY_MIN:
        logger.info(
            f"审核拦截 — 疑似血腥内容 (红色:{blood_ratio:.2%} 连通:{blood_contiguity:.2%})"
        )
        return ModerationResult(
            passed=False,
            reason="检测到图片可能包含血腥暴力内容，已被安全策略拦截。如有误判请联系管理员。",
            faces=num_faces,
            skin_ratio=skin_ratio,
            skin_regions=skin_regions,
            blood_ratio=blood_ratio,
            blood_contiguity=blood_contiguity,
        )

    return ModerationResult(
        passed=True,
        faces=num_faces,
        skin_ratio=skin_ratio,
        skin_regions=skin_regions,
        blood_ratio=blood_ratio,
        blood_contiguity=blood_contiguity,
    )
