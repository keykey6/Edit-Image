import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/long-stitch", tags=["长图拼接"])


@router.post("/process")
async def process(
    files: list[UploadFile] = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    direction = p.get("direction", "vertical")  # vertical / horizontal
    gap = max(0, int(p.get("gap", 0)))
    blend = int(p.get("blend", 0))  # 融合过渡像素

    paths = []
    try:
        images = []
        for f in files:
            fp, fid = save_upload(f)
            paths.append(fp)
            images.append(load_image(fp))

        if direction == "horizontal":
            total_w = sum(img.width for img in images) + gap * (len(images) - 1)
            max_h = max(img.height for img in images)
            canvas = Image.new("RGB", (total_w, max_h), (255, 255, 255))
            x = 0
            for img in images:
                y = (max_h - img.height) // 2
                canvas.paste(img, (x, y))
                x += img.width + gap
        else:
            max_w = max(img.width for img in images)
            total_h = sum(img.height for img in images) + gap * (len(images) - 1)
            canvas = Image.new("RGB", (max_w, total_h), (255, 255, 255))
            y = 0
            for img in images:
                x = (max_w - img.width) // 2
                canvas.paste(img, (x, y))
                y += img.height + gap

        op = _out_path(files[0].filename or "stitch")
        canvas.save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="long_stitch.png")
    finally:
        for fp in paths:
            cleanup_temp(fp)
