import io
import os
import zipfile
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str, suffix: str = "") -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}{suffix}")


router = APIRouter(prefix="/api/batch-process", tags=["批量处理"])


def process_image(img: Image.Image, op: str, p: dict) -> Image.Image:
    """对单张图片执行指定操作。"""
    if op == "compress":
        quality = max(1, min(100, int(p.get("quality", 70))))
        max_size = int(p.get("max_size", 0))
        if max_size > 0:
            w, h = img.size
            ratio = max_size / max(w, h)
            if ratio < 1:
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
        return img

    elif op == "resize":
        width = int(p.get("width", img.width))
        height = int(p.get("height", img.height))
        return img.resize((width, height), Image.LANCZOS)

    elif op == "format_convert":
        fmt = p.get("format", "png").upper()
        if fmt == "JPG":
            fmt = "JPEG"
        return img

    elif op == "grayscale":
        return img.convert("L").convert("RGB")

    elif op == "flip_h":
        return img.transpose(Image.FLIP_LEFT_RIGHT)

    elif op == "flip_v":
        return img.transpose(Image.FLIP_TOP_BOTTOM)

    else:
        return img


@router.post("/process")
async def process(
    files: list[UploadFile] = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    operation = p.get("operation", "compress")
    output_fmt = p.get("output_format", "original")  # "original" or "png"/"jpg"/"webp"

    paths = []
    file_ids = []
    try:
        for f in files:
            fp, fid = save_upload(f)
            paths.append((fp, fid, f.filename or "image.png"))

        zip_path = _out_path(file_ids[0] if file_ids else "batch", "_batch.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for fp, fid, fname in paths:
                img = load_image(fp)
                result = process_image(img, operation, p)

                name, _ = os.path.splitext(fname)
                if output_fmt == "png":
                    ext = ".png"
                    buf = io.BytesIO()
                    result.save(buf, "PNG")
                elif output_fmt == "jpg":
                    ext = ".jpg"
                    buf = io.BytesIO()
                    result.convert("RGB").save(buf, "JPEG", quality=85)
                elif output_fmt == "webp":
                    ext = ".webp"
                    buf = io.BytesIO()
                    result.save(buf, "WEBP", quality=85)
                else:
                    ext = os.path.splitext(fname)[1] or ".png"
                    buf = io.BytesIO()
                    result.save(buf, "PNG")

                buf.seek(0)
                zf.writestr(f"{name}_processed{ext}", buf.getvalue())

        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename="batch_processed.zip",
        )
    finally:
        for fp, _, _ in paths:
            cleanup_temp(fp)
