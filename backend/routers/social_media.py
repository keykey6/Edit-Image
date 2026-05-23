import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/social-media", tags=["社交媒体配图"])

PRESETS = {
    "weibo":       (1200, 800),
    "xiaohongshu": (1080, 1440),
    "wechat":      (1080, 1080),
    "instagram":   (1080, 1080),
    "twitter":     (1200, 675),
    "facebook":    (1200, 630),
}


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    platform = p.get("platform", "instagram")
    w, h = PRESETS.get(platform, PRESETS["instagram"])

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)
        iw, ih = img.size

        target_ratio = w / h
        img_ratio = iw / ih

        if img_ratio > target_ratio:
            # 图片更宽，裁宽度
            new_w = int(ih * target_ratio)
            left = (iw - new_w) // 2
            img = img.crop((left, 0, left + new_w, ih))
        else:
            # 图片更高，裁高度
            new_h = int(iw / target_ratio)
            top = (ih - new_h) // 2
            img = img.crop((0, top, iw, top + new_h))

        img = img.resize((w, h), Image.LANCZOS)

        op = _out_path(file_id)
        img.save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename=f"{platform}.png")
    finally:
        cleanup_temp(filepath)
