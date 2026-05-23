import os
from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont
from config import UPLOAD_DIR
from services.image_utils import parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_text.png")


router = APIRouter(prefix="/api/text-to-image", tags=["文字转图片"])

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/arial.ttf",
]


def _find_font() -> str:
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            return f
    return "arial.ttf"


@router.post("/process")
async def process(
    params: str | None = Form(None),
):
    p = parse_params(params)
    text = p.get("text", "Hello World")
    font_size = int(p.get("font_size", 48))
    color = p.get("color", "#333333")
    bg = p.get("bg", "#ffffff")
    align = p.get("align", "center")  # left/center/right
    width = max(100, min(4000, int(p.get("width", 800))))
    padding = int(p.get("padding", 40))

    import uuid
    file_id = uuid.uuid4().hex

    font_path = _find_font()
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

    # 先测量文字
    temp = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    lines = []
    if tw > width - 2 * padding:
        # 简单自动换行
        current = ""
        for char in text:
            test = current + char
            if draw.textbbox((0, 0), test, font=font)[2] > width - 2 * padding:
                lines.append(current)
                current = char
            else:
                current = test
        if current:
            lines.append(current)
    else:
        lines = [text]

    line_h = th + 8
    total_h = len(lines) * line_h + 2 * padding

    img = Image.new("RGB", (width, total_h), bg)
    draw = ImageDraw.Draw(img)

    y = padding
    for line in lines:
        lw = draw.textbbox((0, 0), line, font=font)[2]
        if align == "center":
            x = (width - lw) // 2
        elif align == "right":
            x = width - lw - padding
        else:
            x = padding
        draw.text((x, y), line, fill=color, font=font)
        y += line_h

    op = _out_path(file_id)
    img.save(op, "PNG")
    return FileResponse(op, media_type="image/png", filename="text_image.png")
