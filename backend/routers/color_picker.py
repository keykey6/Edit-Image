import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
from services.image_utils import save_upload, cleanup_temp, parse_params


router = APIRouter(prefix="/api/color-picker", tags=["取色器"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    x = int(p.get("x", 0))
    y = int(p.get("y", 0))
    sample_size = max(1, int(p.get("sample_size", 5)))  # 周边采样半径

    filepath, file_id = save_upload(file)
    try:
        img = np.array(Image.open(filepath).convert("RGB"))
        h, w = img.shape[:2]

        x = max(0, min(w - 1, x))
        y = max(0, min(h - 1, y))

        half = sample_size // 2
        x1, x2 = max(0, x - half), min(w, x + half + 1)
        y1, y2 = max(0, y - half), min(h, y + half + 1)
        region = img[y1:y2, x1:x2]
        avg = region.mean(axis=(0, 1))

        exact = img[y, x]
        return JSONResponse({
            "point": {"x": x, "y": y},
            "exact": {"r": int(exact[0]), "g": int(exact[1]), "b": int(exact[2]),
                       "hex": f"#{exact[0]:02x}{exact[1]:02x}{exact[2]:02x}"},
            "average": {"r": int(avg[0]), "g": int(avg[1]), "b": int(avg[2]),
                         "hex": f"#{int(avg[0]):02x}{int(avg[1]):02x}{int(avg[2]):02x}"},
        })
    finally:
        cleanup_temp(filepath)
