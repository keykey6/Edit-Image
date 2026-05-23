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


router = APIRouter(prefix="/api/watermark-remove", tags=["水印去除"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    method = p.get("method", "crop")
    margin = int(p.get("margin", 20))

    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        h, w = img.shape[:2]

        if method == "crop":
            m = min(margin, w // 4, h // 4)
            result = img[m:h - m, m:w - m]
        elif method == "blur":
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.rectangle(mask, (0, 0), (w, margin), 255, -1)
            cv2.rectangle(mask, (0, 0), (margin, h), 255, -1)
            cv2.rectangle(mask, (w - margin, 0), (w, h), 255, -1)
            cv2.rectangle(mask, (0, h - margin), (w, h), 255, -1)
            blurred = cv2.GaussianBlur(img, (31, 31), 0)
            mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) // 255
            result = (img * (1 - mask_3ch) + blurred * mask_3ch).astype(np.uint8)
        elif method == "inpaint":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
            mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
            result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        else:
            result = img

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="cleaned.png")
    finally:
        cleanup_temp(filepath)
