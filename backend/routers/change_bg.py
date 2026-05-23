import io
import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from rembg import remove
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/change-bg", tags=["换背景"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    bg_file: UploadFile | None = File(None),
    params: str | None = Form(None),
):
    p = parse_params(params)
    bg_color = p.get("bg_color", "#ffffff")

    filepath, file_id = save_upload(file)
    bg_path = None
    try:
        img = load_image(filepath)
        input_bytes = io.BytesIO()
        img.save(input_bytes, format="PNG")
        input_bytes.seek(0)

        result_bytes = remove(input_bytes.getvalue())
        fg = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

        if bg_file:
            bg_path, _ = save_upload(bg_file)
            bg = load_image(bg_path)
            bg = bg.resize(fg.size, Image.LANCZOS).convert("RGBA")
        else:
            bg = Image.new("RGBA", fg.size, bg_color)

        bg.paste(fg, (0, 0), fg)

        op = _out_path(file_id)
        bg.convert("RGB").save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="newbg.png")
    finally:
        cleanup_temp(filepath)
        if bg_path:
            cleanup_temp(bg_path)
