import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/dpi", tags=["DPI设置"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    dpi_x = int(p.get("dpi_x", 300))
    dpi_y = int(p.get("dpi_y", 300))

    filepath, file_id = save_upload(file)
    try:
        img = Image.open(filepath)
        fmt = img.format or "PNG"
        ext = f".{fmt.lower()}"

        op = _out_path(file_id).replace(".png", ext)
        save_kwargs = {"dpi": (dpi_x, dpi_y)}
        if fmt.upper() == "JPEG":
            save_kwargs["quality"] = 95
        img.save(op, fmt, **save_kwargs)
        return FileResponse(op, media_type=f"image/{fmt.lower()}", filename=f"dpi_{dpi_x}.{fmt.lower()}")
    finally:
        cleanup_temp(filepath)
