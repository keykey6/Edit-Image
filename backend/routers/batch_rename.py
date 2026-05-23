import os
import re
import zipfile
import io
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from config import UPLOAD_DIR
from services.image_utils import save_upload, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}.zip")


router = APIRouter(prefix="/api/batch-rename", tags=["批量重命名"])


@router.post("/process")
async def process(
    files: list[UploadFile] = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    pattern = str(p.get("pattern", "image_{num}"))  # {num} 会被替换
    start_index = int(p.get("start_index", 1))

    paths = []
    try:
        zip_path = _out_path(files[0].filename or "renamed")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for idx, f in enumerate(files):
                fp, fid = save_upload(f)
                paths.append(fp)

                _, ext = os.path.splitext(f.filename or "image.png")
                new_name = pattern.replace("{num}", str(start_index + idx))
                if not new_name.endswith(ext):
                    new_name += ext

                with open(fp, "rb") as src:
                    zf.writestr(new_name, src.read())

        return FileResponse(zip_path, media_type="application/zip", filename="renamed.zip")
    finally:
        for fp in paths:
            cleanup_temp(fp)
