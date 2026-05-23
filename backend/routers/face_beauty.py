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


router = APIRouter(prefix="/api/face-beauty", tags=["人像美颜"])


def skin_smooth(img: np.ndarray, strength: float) -> np.ndarray:
    d = max(5, int(15 * strength))
    sigma = max(10, int(80 * strength))
    return cv2.bilateralFilter(img, d, sigma, sigma)


def whiten(img: np.ndarray, strength: float) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = np.clip(l.astype(np.float32) * (1.0 + strength * 0.3), 0, 255).astype(np.uint8)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


def sharpen(img: np.ndarray, strength: float) -> np.ndarray:
    blurred = cv2.GaussianBlur(img, (0, 0), 3)
    return cv2.addWeighted(img, 1.0 + strength * 0.5, blurred, -strength * 0.5, 0)


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    smooth_strength = max(0.0, min(1.0, float(p.get("smooth", 0.5))))
    whiten_strength = max(0.0, min(1.0, float(p.get("whiten", 0.3))))
    sharpen_strength = max(0.0, min(1.0, float(p.get("sharpen", 0.3))))

    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        if smooth_strength > 0:
            img = skin_smooth(img, smooth_strength)
        if whiten_strength > 0:
            img = whiten(img, whiten_strength)
        if sharpen_strength > 0:
            img = sharpen(img, sharpen_strength)

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="beauty.png")
    finally:
        cleanup_temp(filepath)
