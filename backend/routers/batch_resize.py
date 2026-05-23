import os
import io
import zipfile
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}.zip")


router = APIRouter(prefix="/api/batch-resize", tags=["批量改尺寸"])


@router.post("/process")
async def process(
    files: list[UploadFile] = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    target_w = max(1, int(p.get("width", 800)))
    target_h = max(1, int(p.get("height", 600)))
    mode = p.get("mode", "cover")  # cover / contain / stretch

    paths = []
    try:
        zip_path = _out_path(files[0].filename or "resized")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                fp, fid = save_upload(f)
                paths.append(fp)
                img = load_image(fp)
                iw, ih = img.size

                if mode == "stretch":
                    img = img.resize((target_w, target_h), Image.LANCZOS)
                elif mode == "cover":
                    scale = max(target_w / iw, target_h / ih)
                    new_w, new_h = int(iw * scale), int(ih * scale)
                    img = img.resize((new_w, new_h), Image.LANCZOS)
                    left = (new_w - target_w) // 2
                    top = (new_h - target_h) // 2
                    img = img.crop((left, top, left + target_w, top + target_h))
                else:  # contain
                    scale = min(target_w / iw, target_h / ih)
                    new_w, new_h = int(iw * scale), int(ih * scale)
                    img = img.resize((new_w, new_h), Image.LANCZOS)

                buf = io.BytesIO()
                img.convert("RGB").save(buf, "PNG")
                buf.seek(0)
                zf.writestr(f.filename or f"image.png", buf.getvalue())

        return FileResponse(zip_path, media_type="application/zip", filename="resized.zip")
    finally:
        for fp in paths:
            cleanup_temp(fp)
