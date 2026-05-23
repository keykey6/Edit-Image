import os
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/curve", tags=["曲线调色"])


def _build_curve_lut(points: list) -> np.ndarray:
    """从控制点列表构建256级查找表（线性插值）。"""
    if len(points) < 2:
        return np.arange(256, dtype=np.uint8)
    pts = np.array(points, dtype=np.float32)
    xs = np.linspace(0, 255, 256)
    ys = np.interp(xs, pts[:, 0] * 2.55, np.clip(pts[:, 1] * 2.55, 0, 255))
    return np.clip(ys, 0, 255).astype(np.uint8)


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    # 默认曲线点（直通线）
    r_pts = p.get("r_points", [[0, 0], [100, 100]])
    g_pts = p.get("g_points", [[0, 0], [100, 100]])
    b_pts = p.get("b_points", [[0, 0], [100, 100]])

    filepath, file_id = save_upload(file)
    try:
        img = np.array(Image.open(filepath).convert("RGB"))

        r_lut = _build_curve_lut(r_pts)
        g_lut = _build_curve_lut(g_pts)
        b_lut = _build_curve_lut(b_pts)

        result = np.dstack([
            r_lut[img[:, :, 0]],
            g_lut[img[:, :, 1]],
            b_lut[img[:, :, 2]],
        ])

        op = _out_path(file_id)
        Image.fromarray(result).save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="curve_adjusted.png")
    finally:
        cleanup_temp(filepath)
