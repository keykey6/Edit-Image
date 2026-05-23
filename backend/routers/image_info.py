import os
import math
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image, ExifTags
from services.image_utils import save_upload, cleanup_temp

router = APIRouter(prefix="/api/image-info", tags=["图片信息"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    filepath, _ = save_upload(file)
    try:
        img = Image.open(filepath)
        w, h = img.size
        file_size = os.path.getsize(filepath)

        g = math.gcd(w, h)
        info = {
            "filename": file.filename,
            "format": img.format or "unknown",
            "mode": img.mode,
            "width": w,
            "height": h,
            "file_size_bytes": file_size,
            "file_size_kb": round(file_size / 1024, 1),
            "aspect_ratio": f"{w // g}:{h // g}",
        }

        exif_data = {}
        try:
            exif = img._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                    if isinstance(value, bytes):
                        value = f"<{len(value)} bytes>"
                    exif_data[tag_name] = str(value)
                info["exif"] = exif_data
        except Exception:
            pass

        return JSONResponse({"status": "ok", "data": info})
    finally:
        cleanup_temp(filepath)
