import cv2
import numpy as np
from pyzbar.pyzbar import decode
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
from services.image_utils import save_upload, cleanup_temp, parse_params


router = APIRouter(prefix="/api/qr-decode", tags=["二维码解码"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        results = decode(img)
        codes = []
        for r in results:
            codes.append({
                "type": r.type,
                "data": r.data.decode("utf-8", errors="replace"),
                "rect": {
                    "x": r.rect.left,
                    "y": r.rect.top,
                    "width": r.rect.width,
                    "height": r.rect.height,
                }
            })

        return JSONResponse({
            "found": len(codes),
            "codes": codes,
        })
    finally:
        cleanup_temp(filepath)
