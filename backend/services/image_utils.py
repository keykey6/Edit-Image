import os
import json
import uuid
from fastapi import Form, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR


def parse_params(params_str: str | None = Form(None)) -> dict:
    """Parse JSON params from form data."""
    if params_str:
        try:
            return json.loads(params_str)
        except (json.JSONDecodeError, TypeError):
            pass
    return {}


def save_upload(file: UploadFile) -> tuple[str, str]:
    file_id = uuid.uuid4().hex
    ext = os.path.splitext(file.filename or ".png")[1].lower() or ".png"
    filename = f"{file_id}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    return filepath, file_id


def load_image(path: str) -> Image.Image:
    return Image.open(path).convert("RGB")


def save_image(img: Image.Image, file_id: str, fmt: str = "PNG") -> str:
    """Save PIL image, fmt can be 'JPEG', 'PNG', 'WEBP', 'BMP'. Returns output path."""
    ext = fmt.lower()
    if ext == "jpeg" or ext == "jpg":
        ext = "jpg"
    out_path = os.path.join(UPLOAD_DIR, f"{file_id}_out.{ext}")
    save_kwargs = {}
    if fmt.upper() in ("JPEG", "JPG"):
        img = img.convert("RGB")
        save_kwargs["quality"] = 95
    elif fmt.upper() == "WEBP":
        save_kwargs["quality"] = 90
    img.save(out_path, fmt.upper(), **save_kwargs)
    return out_path


def cleanup_temp(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)


def image_response(path: str, filename: str = "result.png", cleanup_after: bool = False) -> FileResponse:
    """Return FileResponse with proper headers. If cleanup_after, schedule cleanup after response."""
    return FileResponse(
        path,
        media_type="image/png",
        filename=filename,
        background=None if not cleanup_after else None,
    )
