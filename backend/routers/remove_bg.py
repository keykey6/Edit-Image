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


router = APIRouter(prefix="/api/remove-bg", tags=["AI抠图"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    alpha_matting = bool(p.get("alpha_matting", False))

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)

        input_bytes = io.BytesIO()
        img.save(input_bytes, format="PNG")
        input_bytes.seek(0)

        result = remove(input_bytes.getvalue(), alpha_matting=alpha_matting)
        result_img = Image.open(io.BytesIO(result)).convert("RGBA")

        op = _out_path(file_id)
        result_img.save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="nobg.png")
    finally:
        cleanup_temp(filepath)
