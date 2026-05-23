import os
import qrcode
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/qrcode-gen", tags=["二维码生成"])


@router.post("/process")
async def process(
    file: UploadFile | None = File(None),
    params: str | None = Form(None),
):
    p = parse_params(params)
    text = p.get("text", "https://example.com")
    size = int(p.get("size", 300))
    fg_color = p.get("fg_color", "#000000")
    bg_color = p.get("bg_color", "#ffffff")
    box_size = max(4, size // 25)

    import uuid
    fid = uuid.uuid4().hex

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H if file else qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert("RGBA")

    qr_img = qr_img.resize((size, size), Image.LANCZOS)

    if file:
        logo = Image.open(file.file).convert("RGBA")
        logo_size = int(size * 0.22)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        pos = ((size - logo_size) // 2, (size - logo_size) // 2)
        qr_img.paste(logo, pos, logo)

    op = _out_path(fid)
    qr_img.save(op, "PNG")
    return FileResponse(op, media_type="image/png", filename="qrcode.png")
