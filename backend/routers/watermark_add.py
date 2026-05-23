import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str, fmt: str = "png") -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.{fmt}")


def _load_font(size: int):
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


router = APIRouter(prefix="/api/watermark-add", tags=["水印添加"])


def add_text_watermark(img: Image.Image, text: str, position: str,
                       font_size: int, color: str, opacity: float) -> Image.Image:
    result = img.convert("RGBA")
    overlay = Image.new("RGBA", result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = _load_font(font_size)

    if position == "tiled":
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        spacing_x = tw + 100
        spacing_y = th + 80
        for y in range(0, result.height, spacing_y):
            for x in range(0, result.width, spacing_x):
                draw.text((x, y), text, font=font, fill=color)
    else:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        margin = 30
        positions = {
            "top-left": (margin, margin),
            "top-right": (result.width - tw - margin, margin),
            "center": ((result.width - tw) // 2, (result.height - th) // 2),
            "bottom-left": (margin, result.height - th - margin),
            "bottom-right": (result.width - tw - margin, result.height - th - margin),
        }
        x, y = positions.get(position, positions["bottom-right"])
        draw.text((x, y), text, font=font, fill=color)

    alpha = overlay.split()[3].point(lambda p: int(p * opacity))
    overlay.putalpha(alpha)
    return Image.alpha_composite(result, overlay)


def add_image_watermark(img: Image.Image, wm: Image.Image, position: str,
                        scale: float, opacity: float) -> Image.Image:
    result = img.convert("RGBA")
    w, h = result.size
    wm_w, wm_h = int(wm.width * scale), int(wm.height * scale)
    wm = wm.resize((wm_w, wm_h), Image.LANCZOS).convert("RGBA")

    if opacity < 1.0:
        alpha = wm.split()[3].point(lambda p: int(p * opacity))
        wm.putalpha(alpha)

    margin = 20
    pos_map = {
        "top-left": (margin, margin),
        "top-right": (w - wm_w - margin, margin),
        "center": ((w - wm_w) // 2, (h - wm_h) // 2),
        "bottom-left": (margin, h - wm_h - margin),
        "bottom-right": (w - wm_w - margin, h - wm_h - margin),
        "tiled": None,
    }

    if position == "tiled":
        spacing_x = wm_w + 60
        spacing_y = wm_h + 40
        for y in range(0, h, spacing_y):
            for x in range(0, w, spacing_x):
                result.paste(wm, (x, y), wm)
    else:
        x, y = pos_map.get(position, pos_map["bottom-right"])
        result.paste(wm, (x, y), wm)

    return result


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    watermark_file: UploadFile | None = File(None),
    params: str | None = Form(None),
):
    p = parse_params(params)
    wm_type = p.get("type", "text")

    filepath, file_id = save_upload(file)
    wm_path = None
    try:
        img = load_image(filepath)

        if wm_type == "image" and watermark_file:
            wm_path, _ = save_upload(watermark_file)
            wm = Image.open(wm_path).convert("RGBA")
            position = p.get("position", "bottom-right")
            scale = float(p.get("scale", 0.15))
            opacity = float(p.get("opacity", 0.5))
            result = add_image_watermark(img, wm, position, scale, opacity)
        else:
            text = p.get("text", "Watermark")
            position = p.get("position", "bottom-right")
            font_size = int(p.get("font_size", 36))
            color = p.get("color", "#ffffff")
            opacity = float(p.get("opacity", 0.5))
            result = add_text_watermark(img, text, position, font_size, color, opacity)

        op = _out_path(file_id)
        result.convert("RGB").save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="watermarked.png")
    finally:
        cleanup_temp(filepath)
        if wm_path:
            cleanup_temp(wm_path)
