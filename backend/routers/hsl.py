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


router = APIRouter(prefix="/api/hsl", tags=["HSL调色"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    hue = float(p.get("hue", 0))         # -180 ~ 180
    saturation = float(p.get("saturation", 1.0))  # 0 ~ 3
    lightness = float(p.get("lightness", 1.0))    # 0 ~ 3

    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS).astype(np.float32)

        hls[:, :, 0] = (hls[:, :, 0] + hue) % 180
        hls[:, :, 1] = np.clip(hls[:, :, 1] * lightness, 0, 255)
        hls[:, :, 2] = np.clip(hls[:, :, 2] * saturation, 0, 255)

        result = cv2.cvtColor(hls.astype(np.uint8), cv2.COLOR_HLS2BGR)

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="hsl_adjusted.png")
    finally:
        cleanup_temp(filepath)
