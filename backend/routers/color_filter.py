import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageEnhance
from services.image_utils import save_upload, load_image, save_image, cleanup_temp, parse_params

PRESETS = {
    "warm": {"temperature": 40, "saturation": 1.1, "brightness": 1.05},
    "cool": {"temperature": -40, "saturation": 0.9, "brightness": 1.0},
    "bw": {"saturation": 0.0, "contrast": 1.2},
    "vintage": {"saturation": 0.7, "contrast": 1.1, "temperature": 20, "brightness": 0.95},
    "japanese": {"saturation": 0.85, "temperature": -10, "brightness": 1.1, "contrast": 0.95},
}

router = APIRouter(prefix="/api/color-filter", tags=["调色滤镜"])


def apply_temperature(img: Image.Image, value: int) -> Image.Image:
    """色温调整。正值=暖色, 负值=冷色。"""
    if value == 0:
        return img
    arr = np.array(img, dtype=np.float32)
    if value > 0:
        arr[:, :, 0] += value * 1.5  # R+
        arr[:, :, 2] -= value * 0.5  # B-
    else:
        arr[:, :, 2] += abs(value) * 1.5  # B+
        arr[:, :, 0] -= abs(value) * 0.5  # R-
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    preset = p.get("preset", "")
    brightness = float(p.get("brightness", 1.0))
    contrast = float(p.get("contrast", 1.0))
    saturation = float(p.get("saturation", 1.0))
    temperature = int(p.get("temperature", 0))

    if preset and preset in PRESETS:
        cfg = PRESETS[preset]
        brightness = float(p.get("brightness", cfg.get("brightness", 1.0)))
        contrast = float(p.get("contrast", cfg.get("contrast", 1.0)))
        saturation = float(p.get("saturation", cfg.get("saturation", 1.0)))
        temperature = int(p.get("temperature", cfg.get("temperature", 0)))

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)

        if brightness != 1.0:
            img = ImageEnhance.Brightness(img).enhance(brightness)
        if contrast != 1.0:
            img = ImageEnhance.Contrast(img).enhance(contrast)
        if saturation != 1.0:
            img = ImageEnhance.Color(img).enhance(saturation)
        if temperature != 0:
            img = apply_temperature(img, temperature)

        out_path = save_image(img, file_id)
        return FileResponse(out_path, media_type="image/png", filename="filtered.png")
    finally:
        cleanup_temp(filepath)
