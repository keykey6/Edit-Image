import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
from sklearn.cluster import KMeans
from services.image_utils import save_upload, cleanup_temp, parse_params


router = APIRouter(prefix="/api/color-analysis", tags=["色彩分析"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    k = max(2, min(20, int(p.get("k", 5))))

    filepath, file_id = save_upload(file)
    try:
        img = Image.open(filepath).convert("RGB")
        # 缩放加速
        small = img.resize((150, 150))
        pixels = np.array(small).reshape(-1, 3)

        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_.astype(int)
        labels = kmeans.labels_

        # 按出现频率排序
        counts = np.bincount(labels)
        order = np.argsort(-counts)
        palette = [
            {"hex": f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}",
             "rgb": [int(c[0]), int(c[1]), int(c[2])],
             "ratio": round(counts[i] / len(labels) * 100, 1)}
            for i in order
            for c in [centers[i]]
        ]

        return JSONResponse({"colors": palette})
    finally:
        cleanup_temp(filepath)
