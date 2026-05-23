import io
import os
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw
from rembg import remove
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/suit-change", tags=["证件照换装"])

TEMPLATE_COLORS = {
    "black": (40, 40, 45),
    "navy": (30, 40, 80),
    "gray": (100, 100, 110),
    "white": (220, 220, 225),
}


def create_suit_template(w: int, h: int, color: tuple) -> Image.Image:
    """用纯色+领口画一个简单的正装模板。"""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = w // 2, int(h * 0.55)
    collar_w, collar_h = int(w * 0.38), int(h * 0.28)

    # 身体矩形
    body_top = int(h * 0.38)
    draw.rectangle([0, body_top, w, h], fill=color)

    # V形领口（用三角形透明区域模拟）
    collar_poly = [
        (cx, cy + int(collar_h * 0.3)),
        (cx - collar_w, cy - collar_h),
        (cx + collar_w, cy - collar_h),
    ]
    draw.polygon(collar_poly, fill=(0, 0, 0, 0))

    # 白色衬衫领子
    shift = int(collar_w * 0.08)
    collar_white = [
        (cx, cy + int(collar_h * 0.2)),
        (cx - collar_w + shift, cy - collar_h + shift),
        (cx + collar_w - shift, cy - collar_h + shift),
    ]
    draw.polygon(collar_white, fill=(240, 240, 245, 255))

    # 领带
    tie_w, tie_h = int(w * 0.04), int(h * 0.22)
    tie_top = cy - int(collar_h * 0.3)
    tie_color = (180, 30, 30, 255)
    draw.rectangle([cx - tie_w, tie_top, cx + tie_w, tie_top + tie_h], fill=tie_color)
    # 领带结
    draw.polygon(
        [(cx, tie_top - 5), (cx - tie_w - 2, tie_top + 8), (cx + tie_w + 2, tie_top + 8)],
        fill=tie_color,
    )

    return img


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    suit_color = p.get("color", "black")
    color = TEMPLATE_COLORS.get(suit_color, TEMPLATE_COLORS["black"])

    filepath, file_id = save_upload(file)
    try:
        pil_img = load_image(filepath)
        w, h = pil_img.size

        # 抠出人像
        input_bytes = io.BytesIO()
        pil_img.save(input_bytes, format="PNG")
        input_bytes.seek(0)
        nobg_bytes = remove(input_bytes.getvalue())
        person = Image.open(io.BytesIO(nobg_bytes)).convert("RGBA")

        # 创建模板（1.3倍宽，留余量）
        template_w = int(w * 1.1)
        template_h = h
        template = create_suit_template(template_w, template_h, color)

        # 把人像贴到模板上（居中偏上）
        offset_x = (template_w - w) // 2
        template.paste(person, (offset_x, 0), person)

        # 裁剪到合理范围
        result = template.crop((0, 0, template_w, template_h))

        op = _out_path(file_id)
        result.convert("RGB").save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="suit_changed.png")
    finally:
        cleanup_temp(filepath)
