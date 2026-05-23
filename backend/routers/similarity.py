import imagehash
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
from services.image_utils import save_upload, cleanup_temp, parse_params


router = APIRouter(prefix="/api/similarity", tags=["图片相似度"])

METHODS = {
    "phash": imagehash.phash,
    "dhash": imagehash.dhash,
    "ahash": imagehash.average_hash,
    "whash": imagehash.whash,
}


@router.post("/process")
async def process(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    method_key = p.get("method", "phash")

    f1, _ = save_upload(file1)
    f2, _ = save_upload(file2)
    try:
        img1 = Image.open(f1).convert("RGB")
        img2 = Image.open(f2).convert("RGB")

        hash_fn = METHODS.get(method_key, imagehash.phash)
        h1 = hash_fn(img1)
        h2 = hash_fn(img2)
        diff = int(h1 - h2)  # 汉明距离

        similar = diff <= 10
        return JSONResponse({
            "method": method_key,
            "hash1": str(h1),
            "hash2": str(h2),
            "hamming_distance": diff,
            "similar": similar,
            "similarity_percent": round(max(0, 100 - diff * 1.5), 1),
        })
    finally:
        cleanup_temp(f1)
        cleanup_temp(f2)
