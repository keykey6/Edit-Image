import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/privacy-erase", tags=["隐私信息擦除"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    erase_exif = bool(p.get("erase_exif", True))
    erase_thumbnail = bool(p.get("erase_thumbnail", True))

    filepath, file_id = save_upload(file)
    try:
        img = Image.open(filepath)

        # 重建干净图片（剥离所有元数据）
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()))

        # 如果不需要擦除缩略图且存在缩略图则保留
        if not erase_thumbnail and hasattr(img, 'info') and 'thumbnail' in img.info:
            clean.info['thumbnail'] = img.info['thumbnail']

        op = _out_path(file_id)
        if erase_exif:
            clean.save(op, "PNG")
        else:
            # 保留 EXIF 但清理其他元数据
            exif = img.info.get('exif', b'')
            clean.save(op, "PNG", exif=exif)

        return FileResponse(op, media_type="image/png", filename="privacy_cleaned.png")
    finally:
        cleanup_temp(filepath)
