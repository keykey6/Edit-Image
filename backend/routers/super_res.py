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


router = APIRouter(prefix="/api/super-res", tags=["分辨率放大"])


def usm_sharpen(img: np.ndarray, amount: float = 1.0) -> np.ndarray:
    blurred = cv2.GaussianBlur(img, (0, 0), 2.0)
    return cv2.addWeighted(img, 1.0 + amount, blurred, -amount, 0)


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    scale = max(1.0, min(4.0, float(p.get("scale", 2.0))))
    sharpen_amount = max(0.0, min(1.0, float(p.get("sharpen", 0.5))))

    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        h, w = img.shape[:2]
        new_w, new_h = int(w * scale), int(h * scale)
        result = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

        if sharpen_amount > 0:
            result = usm_sharpen(result, sharpen_amount)

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename=f"upscaled_{scale}x.png")
    finally:
        cleanup_temp(filepath)
