import os
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw
from config import UPLOAD_DIR
from services.image_utils import save_upload, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_hist.png")


router = APIRouter(prefix="/api/histogram", tags=["图片直方图"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    filepath, file_id = save_upload(file)
    try:
        img = np.array(Image.open(filepath).convert("RGB"))

        h, w = 300, 512
        chart = Image.new("RGB", (w, h), (30, 30, 30))
        draw = ImageDraw.Draw(chart)

        colors = [(255, 80, 80), (80, 255, 80), (80, 80, 255)]
        max_count = 0
        hists = []
        for c in range(3):
            hist, _ = np.histogram(img[:, :, c].ravel(), bins=256, range=(0, 256))
            hists.append(hist)
            max_count = max(max_count, hist.max())

        for c in range(3):
            hist = hists[c]
            color = colors[c]
            for i in range(1, 256):
                y1 = h - 1 - int(hist[i - 1] / max_count * (h - 20)) - 10
                y2 = h - 1 - int(hist[i] / max_count * (h - 20)) - 10
                x1 = int((i - 1) * w / 256)
                x2 = int(i * w / 256)
                draw.rectangle([x1, y1, x2, h - 11], fill=color + (80,))

        op = _out_path(file_id)
        chart.save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="histogram.png")
    finally:
        cleanup_temp(filepath)
