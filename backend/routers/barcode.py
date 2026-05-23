import os
import io
import barcode
from barcode.writer import ImageWriter
from fastapi import APIRouter, Form
from fastapi.responses import FileResponse, JSONResponse
from config import UPLOAD_DIR
from services.image_utils import parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_barcode.png")


router = APIRouter(prefix="/api/barcode", tags=["条形码生成"])

FORMATS = {
    "ean13": barcode.EAN13,
    "ean8": barcode.EAN8,
    "upca": barcode.UPCA,
    "code128": barcode.Code128,
    "code39": barcode.Code39,
    "isbn13": barcode.ISBN13,
}


@router.post("/process")
async def process(
    params: str | None = Form(None),
):
    p = parse_params(params)
    text = str(p.get("text", "123456789012"))  # EAN13 needs 12 digits
    fmt = p.get("format", "code128")
    width = float(p.get("width", 0.3))
    height = float(p.get("height", 20))

    import uuid
    file_id = uuid.uuid4().hex

    try:
        cls = FORMATS.get(fmt, barcode.Code128)
        writer = ImageWriter()
        writer.set_options({"module_width": width, "module_height": height})

        buf = io.BytesIO()
        code = cls(text, writer=writer)
        code.write(buf)
        buf.seek(0)

        op = _out_path(file_id)
        with open(op, "wb") as f:
            f.write(buf.read())

        return FileResponse(op, media_type="image/png", filename=f"barcode_{fmt}.png")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


