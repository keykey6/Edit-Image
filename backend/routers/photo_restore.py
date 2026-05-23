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


router = APIRouter(prefix="/api/photo-restore", tags=["老照片修复"])


def denoise(img: np.ndarray, strength: float) -> np.ndarray:
    h = max(3, int(10 * strength))
    return cv2.fastNlMeansDenoisingColored(img, None, h, h, 7, 21)


def enhance_contrast(img: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


def auto_white_balance(img: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    a = cv2.addWeighted(a, 1.0, np.full_like(a, 128), -0.15, 0)
    b = cv2.addWeighted(b, 1.0, np.full_like(b, 128), -0.15, 0)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


def remove_scratches(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 100)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(edges, kernel, iterations=1)
    return cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)


def color_correct(img: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    low, high = np.percentile(l, 1), np.percentile(l, 99)
    if high > low:
        l = np.clip((l - low) * 255.0 / (high - low), 0, 255).astype(np.uint8)
    return cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    denoise_strength = max(0.0, min(1.0, float(p.get("denoise", 0.5))))
    fix_scratches = bool(p.get("fix_scratches", True))
    correct_color = bool(p.get("correct_color", True))

    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        img = color_correct(img)
        img = enhance_contrast(img)

        if denoise_strength > 0:
            img = denoise(img, denoise_strength)

        if correct_color:
            img = auto_white_balance(img)

        if fix_scratches:
            img = remove_scratches(img)

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="restored.png")
    finally:
        cleanup_temp(filepath)
