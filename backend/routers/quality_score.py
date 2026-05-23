import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
from services.image_utils import save_upload, cleanup_temp, parse_params


router = APIRouter(prefix="/api/quality-score", tags=["图片质量评分"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    filepath, file_id = save_upload(file)
    try:
        img = cv2.imread(filepath)
        if img is None:
            pil_img = Image.open(filepath).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 清晰度：Laplacian方差
        lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        sharpness_score = min(100, round(lap_var / 10, 1))

        # 噪点：高频分量的标准差
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        noise = cv2.absdiff(gray, blurred)
        noise_level = float(np.std(noise))
        noise_score = max(0, min(100, round(100 - noise_level * 5, 1)))

        # 色彩丰富度：RGB三通道标准差
        stds = [float(np.std(img[:, :, c])) for c in range(3)]
        color_richness = round(sum(stds) / 3, 1)
        color_score = min(100, round(color_richness / 0.8, 1))

        # 综合评分
        overall = round((sharpness_score * 0.4 + noise_score * 0.3 + color_score * 0.3), 1)

        return JSONResponse({
            "overall_score": overall,
            "sharpness_score": sharpness_score,
            "noise_score": noise_score,
            "color_score": color_score,
            "details": {
                "laplacian_variance": round(lap_var, 2),
                "noise_std": round(noise_level, 2),
                "color_richness": color_richness,
            }
        })
    finally:
        cleanup_temp(filepath)
