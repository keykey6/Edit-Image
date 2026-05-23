import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageFilter
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/shadow", tags=["阴影倒影"])


def _make_shadow(img: Image.Image, offset: int, opacity: float, blur: int) -> Image.Image:
    """生成图片的倒影（垂直翻转 + 渐变透明 + 模糊）。"""
    reflected = img.transpose(Image.FLIP_TOP_BOTTOM)
    w, h = reflected.size
    fade_h = h  # 全部渐变

    alpha_mask = Image.new("L", (w, h), 0)
    for y in range(fade_h):
        alpha = int(opacity * 255 * (1 - y / fade_h))
        for x in range(w):
            alpha_mask.putpixel((x, y), alpha)

    reflected.putalpha(alpha_mask)
    if blur > 0:
        reflected = reflected.filter(ImageFilter.GaussianBlur(blur))
    return reflected


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    offset = max(0, int(p.get("offset", 20)))       # 倒影间距
    opacity = max(0.1, min(1.0, float(p.get("opacity", 0.4))))
    blur = max(0, int(p.get("blur", 3)))

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath).convert("RGBA")
        shadow = _make_shadow(img, offset, opacity, blur)

        w, h = img.size
        sw, sh = shadow.size
        canvas = Image.new("RGBA", (max(w, sw), h + offset + sh), (255, 255, 255, 255))
        canvas.paste(img, (0, 0), img)
        canvas.paste(shadow, ((max(w, sw) - sw) // 2, h + offset), shadow)

        op = _out_path(file_id)
        canvas.convert("RGB").save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="shadow.png")
    finally:
        cleanup_temp(filepath)
