from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw
from services.image_utils import save_upload, load_image, save_image, cleanup_temp, parse_params


def create_rounded_mask(size, radius):
    w, h = size
    mask = Image.new("L", (w * 3, h * 3), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, w * 3, h * 3], radius=radius * 3, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    return mask


router = APIRouter(prefix="/api/rounded-border", tags=["圆角边框"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    radius = max(0, int(p.get("radius", 40)))
    border_size = max(1, int(p.get("border_size", 0)))
    border_color = p.get("border_color", "#ffffff")

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)
        w, h = img.size

        mask = create_rounded_mask((w, h), radius)
        img.putalpha(mask)

        if border_size > 0:
            bg = Image.new("RGBA", (w + border_size * 2, h + border_size * 2), border_color)
            bg_mask = create_rounded_mask((w + border_size * 2, h + border_size * 2), radius + border_size)
            bg.paste(img, (border_size, border_size), mask)
            out_path = save_image(bg.convert("RGB"), file_id)
        else:
            out_path = save_image(img, file_id)

        return FileResponse(out_path, media_type="image/png", filename="rounded.png")
    finally:
        cleanup_temp(filepath)
