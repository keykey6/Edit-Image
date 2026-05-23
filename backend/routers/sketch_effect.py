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


router = APIRouter(prefix="/api/sketch-effect", tags=["素描漫画"])


def pencil_sketch(img_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


def canny_sketch(img_bgr: np.ndarray, low: int = 50, high: int = 150) -> np.ndarray:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, low, high)
    return cv2.cvtColor(255 - edges, cv2.COLOR_GRAY2BGR)


def comic_effect(img_bgr: np.ndarray) -> np.ndarray:
    color = cv2.bilateralFilter(img_bgr, 9, 75, 75)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return cv2.bitwise_and(color, edges_color)


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    style = p.get("style", "pencil")

    filepath, file_id = save_upload(file)
    try:
        img_bgr = cv2.imread(filepath)
        if img_bgr is None:
            pil_img = Image.open(filepath).convert("RGB")
            img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        if style == "canny":
            low = int(p.get("low_threshold", 50))
            high = int(p.get("high_threshold", 150))
            result = canny_sketch(img_bgr, low, high)
            filename = "canny_sketch.png"
        elif style == "comic":
            result = comic_effect(img_bgr)
            filename = "comic.png"
        else:
            result = pencil_sketch(img_bgr)
            filename = "pencil_sketch.png"

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename=filename)
    finally:
        cleanup_temp(filepath)
