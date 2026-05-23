import os
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/dehaze", tags=["去雾提亮"])


def dehaze_clahe(img_bgr: np.ndarray, clip_limit: float = 2.0, tile_size: int = 8) -> np.ndarray:
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def contrast_stretch(img_bgr: np.ndarray, low_pct: float = 1.0, high_pct: float = 99.0) -> np.ndarray:
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    low = np.percentile(l, low_pct)
    high = np.percentile(l, high_pct)
    if high > low:
        l = np.clip((l - low) * 255.0 / (high - low), 0, 255).astype(np.uint8)
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    strength = max(0.0, min(2.0, float(p.get("strength", 1.0))))
    clip_limit = float(p.get("clip_limit", 2.0))
    tile_size = int(p.get("tile_size", 8))

    filepath, file_id = save_upload(file)
    try:
        img_bgr = cv2.imread(filepath)
        if img_bgr is None:
            pil_img = Image.open(filepath).convert("RGB")
            img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        enhanced = dehaze_clahe(img_bgr, clip_limit, tile_size)
        enhanced = contrast_stretch(enhanced)

        if strength != 1.0:
            enhanced = cv2.addWeighted(img_bgr, 1.0 - strength, enhanced, strength, 0)

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="dehazed.png")
    finally:
        cleanup_temp(filepath)
