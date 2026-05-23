import os
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/blur-mosaic", tags=["模糊打码"])


def gaussian_blur(img: np.ndarray, kernel: int) -> np.ndarray:
    k = kernel if kernel % 2 == 1 else kernel + 1
    return cv2.GaussianBlur(img, (k, k), 0)


def mosaic(img: np.ndarray, block_size: int) -> np.ndarray:
    h, w = img.shape[:2]
    bs = max(2, block_size)
    small = cv2.resize(img, (w // bs, h // bs), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)


def apply_to_regions(img: np.ndarray, regions: list, func, **kwargs) -> np.ndarray:
    result = img.copy()
    for r in regions:
        x, y, rw, rh = int(r["x"]), int(r["y"]), int(r["width"]), int(r["height"])
        x, y = max(0, x), max(0, y)
        rw, rh = min(img.shape[1] - x, rw), min(img.shape[0] - y, rh)
        if rw > 0 and rh > 0:
            roi = img[y:y + rh, x:x + rw]
            result[y:y + rh, x:x + rw] = func(roi, **kwargs)
    return result


def detect_faces(img: np.ndarray) -> list:
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 4)
    return [{"x": f[0], "y": f[1], "width": f[2], "height": f[3]} for f in faces]


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    blur_type = p.get("type", "gaussian")
    kernel_size = int(p.get("kernel_size", 15))
    block_size = int(p.get("block_size", 10))
    regions = p.get("regions", [])
    face_detect = bool(p.get("face_detect", False))

    if face_detect:
        blur_type = "mosaic"

    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        if face_detect:
            face_regions = detect_faces(img)
            regions = list(regions) + face_regions

        if not regions:
            if blur_type == "gaussian":
                result = gaussian_blur(img, kernel_size)
            else:
                result = mosaic(img, block_size)
        else:
            func = gaussian_blur if blur_type == "gaussian" else mosaic
            kw = {"kernel": kernel_size} if blur_type == "gaussian" else {"block_size": block_size}
            result = apply_to_regions(img, regions, func, **kw)

        op = _out_path(file_id)
        Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="blurred.png")
    finally:
        cleanup_temp(filepath)
