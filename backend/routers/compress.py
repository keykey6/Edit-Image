import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params

router = APIRouter(prefix="/api/compress", tags=["图片压缩"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    quality = max(1, min(100, int(p.get("quality", 70))))
    max_size = int(p.get("max_size", 0))

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)

        if max_size > 0:
            w, h = img.size
            longest = max(w, h)
            if longest > max_size:
                ratio = max_size / longest
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

        ext = ".jpg"
        out_path = os.path.join(os.path.dirname(filepath), f"{file_id}_out{ext}")
        img.save(out_path, "JPEG", quality=quality, optimize=True)

        return FileResponse(out_path, media_type="image/jpeg", filename=f"compressed{ext}")
    finally:
        cleanup_temp(filepath)
