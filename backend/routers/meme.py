import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_meme.png")


router = APIRouter(prefix="/api/meme", tags=["表情包制作"])

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/impact.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def _get_font(size: int) -> ImageFont.FreeTypeFont:
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    top_text = p.get("top_text", "")
    bottom_text = p.get("bottom_text", "")
    font_size_ratio = float(p.get("font_size_ratio", 0.1))

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)
        w, h = img.size
        font_size = max(16, int(h * font_size_ratio))
        font = _get_font(font_size)

        # 描边效果
        def draw_stroked_text(draw, text, position, font, text_color, stroke_color, stroke_width=3):
            x, y = position
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), text, fill=stroke_color, font=font)
            draw.text((x, y), text, fill=text_color, font=font)

        draw = ImageDraw.Draw(img)

        if top_text:
            bbox = draw.textbbox((0, 0), top_text, font=font)
            tw = bbox[2] - bbox[0]
            x = (w - tw) // 2
            draw_stroked_text(draw, top_text, (x, 10), font, (255, 255, 255), (0, 0, 0))

        if bottom_text:
            bbox = draw.textbbox((0, 0), bottom_text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            x = (w - tw) // 2
            draw_stroked_text(draw, bottom_text, (x, h - th - 15), font, (255, 255, 255), (0, 0, 0))

        op = _out_path(file_id)
        img.save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="meme.png")
    finally:
        cleanup_temp(filepath)
