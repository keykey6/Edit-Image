import os
import img2pdf
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from config import UPLOAD_DIR
from services.image_utils import save_upload, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}.pdf")


router = APIRouter(prefix="/api/to-pdf", tags=["图片转PDF"])


@router.post("/process")
async def process(
    files: list[UploadFile] = File(...),
    params: str | None = Form(None),
):
    paths = []
    try:
        img_paths = []
        for f in files:
            fp, fid = save_upload(f)
            paths.append(fp)
            img_paths.append(fp)

        pdf_bytes = img2pdf.convert(img_paths)

        op = _out_path(files[0].filename or "output")
        with open(op, "wb") as f:
            f.write(pdf_bytes)

        return FileResponse(op, media_type="application/pdf", filename="converted.pdf")
    finally:
        for fp in paths:
            cleanup_temp(fp)
