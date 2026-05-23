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


router = APIRouter(prefix="/api/perspective", tags=["透视矫正"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    # 原图四点: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]] (左上/右上/右下/左下)
    src_pts = p.get("src_points", None)
    out_w = int(p.get("out_width", 800))
    out_h = int(p.get("out_height", 600))

    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        h, w = img.shape[:2]

        if src_pts and len(src_pts) == 4:
            src = np.float32(src_pts)
        else:
            # 默认四角（不变换）
            margin = min(w, h) // 10
            src = np.float32([
                [margin, margin],
                [w - margin, margin],
                [w - margin, h - margin],
                [margin, h - margin],
            ])

        dst = np.float32([
            [0, 0],
            [out_w - 1, 0],
            [out_w - 1, out_h - 1],
            [0, out_h - 1],
        ])

        matrix = cv2.getPerspectiveTransform(src, dst)
        result = cv2.warpPerspective(img, matrix, (out_w, out_h))

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="perspective_corrected.png")
    finally:
        cleanup_temp(filepath)
