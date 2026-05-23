from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from services.image_utils import save_upload, load_image, save_image, cleanup_temp, parse_params

SUPPORTED_FORMATS = {"jpeg", "jpg", "png", "webp", "bmp"}
MIME_MAP = {"jpeg": "image/jpeg", "jpg": "image/jpeg", "png": "image/png", "webp": "image/webp", "bmp": "image/bmp"}

router = APIRouter(prefix="/api/format-convert", tags=["格式转换"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    target = p.get("format", "png").lower()
    if target not in SUPPORTED_FORMATS:
        target = "png"

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)
        out_path = save_image(img, file_id, fmt=target)
        mime = MIME_MAP.get(target, "image/png")
        return FileResponse(out_path, media_type=mime, filename=f"converted.{target}")
    finally:
        cleanup_temp(filepath)
