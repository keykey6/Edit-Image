import io
import os
import tempfile
import shutil
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from rembg import remove
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


ID_SIZES = {
    "1inch": (295, 413, "25×35mm"),
    "2inch": (413, 579, "35×49mm"),
    "large1inch": (390, 567, "33×48mm"),
}

STANDARD_COLORS = {
    "white": "#ffffff",
    "blue": "#438edb",
    "red": "#cc0000",
    "light_blue": "#6599d5",
}

router = APIRouter(prefix="/api/id-photo", tags=["证件照"])

_cascade = None


def _get_cascade():
    global _cascade
    if _cascade is not None:
        return _cascade
    try:
        src = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        tmp = os.path.join(tempfile.gettempdir(), "cv2_face_cascade.xml")
        if not os.path.exists(tmp):
            with open(src, "rb") as fsrc:
                with open(tmp, "wb") as fdst:
                    fdst.write(fsrc.read())
        _cascade = cv2.CascadeClassifier(tmp)
        return _cascade
    except Exception:
        _cascade = False
        return None


def detect_face_region(img_bgr: np.ndarray) -> tuple | None:
    cascade = _get_cascade()
    if cascade is None or cascade.empty():
        return None
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    if len(faces) == 0:
        return None
    x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
    return x, y, fw, fh


def crop_id_photo(img: Image.Image, face_rect: tuple, target_w: int, target_h: int) -> Image.Image:
    w, h = img.size
    fx, fy, fw, fh = face_rect
    face_center_x = fx + fw // 2
    face_top = fy

    headroom = int(fh * 0.4)
    chin_room = int(fh * 0.6)
    crop_top = max(0, face_top - headroom)
    crop_bottom = min(h, fy + fh + chin_room)
    crop_h = crop_bottom - crop_top

    crop_w = int(crop_h * target_w / target_h)
    crop_left = max(0, face_center_x - crop_w // 2)
    if crop_left + crop_w > w:
        crop_left = max(0, w - crop_w)

    return img.crop((crop_left, crop_top, crop_left + crop_w, crop_h))


def center_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    w, h = img.size
    ratio = target_w / target_h
    if w / h > ratio:
        new_w = int(h * ratio)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / ratio)
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))


def build_print_layout(single: Image.Image, target_w: int, target_h: int) -> Image.Image:
    paper_w, paper_h = 1200, 1800
    cols = paper_w // target_w
    rows = paper_h // target_h
    paper = Image.new("RGB", (paper_w, paper_h), "#ffffff")
    for r in range(rows):
        for c in range(cols):
            px, py = c * target_w, r * target_h
            paper.paste(single, (px, py))
    return paper


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    size_key = p.get("size", "1inch")
    bg_name = p.get("bg", "white")
    layout = p.get("layout", "single")
    bg_color = STANDARD_COLORS.get(bg_name, "#ffffff")

    tw, th, _ = ID_SIZES.get(size_key, ID_SIZES["1inch"])

    filepath, file_id = save_upload(file)
    try:
        pil_img = load_image(filepath)
        img_bgr = cv2.imread(filepath)
        if img_bgr is None:
            img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        face_rect = detect_face_region(img_bgr)

        if face_rect:
            cropped = crop_id_photo(pil_img, face_rect, tw, th)
        else:
            cropped = center_crop(pil_img, tw, th)

        cropped = cropped.resize((tw, th), Image.LANCZOS)

        input_bytes = io.BytesIO()
        cropped.save(input_bytes, format="PNG")
        input_bytes.seek(0)
        nobg_bytes = remove(input_bytes.getvalue())
        fg = Image.open(io.BytesIO(nobg_bytes)).convert("RGBA")

        bg = Image.new("RGBA", (tw, th), bg_color)
        bg.paste(fg, (0, 0), fg)
        single = bg.convert("RGB")

        op = _out_path(file_id)
        if layout == "print":
            print_img = build_print_layout(single, tw, th)
            print_img.save(op, "PNG")
            return FileResponse(op, media_type="image/png", filename="id_photo_print.png")
        else:
            single.save(op, "PNG")
            return FileResponse(op, media_type="image/png", filename=f"id_photo_{size_key}.png")
    finally:
        cleanup_temp(filepath)
