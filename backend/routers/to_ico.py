import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}.ico")


router = APIRouter(prefix="/api/to-ico", tags=["图片转ICO"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    sizes = p.get("sizes", [16, 32, 48, 64, 128, 256])

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)
        # 生成多个尺寸
        icons = []
        for s in sizes:
            resized = img.resize((int(s), int(s)), Image.LANCZOS)
            icons.append(resized)

        op = _out_path(file_id)
        icons[0].save(op, "ICO", sizes=[(i.width, i.height) for i in icons[1:]], append_images=icons[1:])
        return FileResponse(op, media_type="image/x-icon", filename="favicon.ico")
    finally:
        cleanup_temp(filepath)
