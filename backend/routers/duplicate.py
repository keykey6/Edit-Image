import imagehash
from itertools import combinations
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from PIL import Image
from services.image_utils import save_upload, cleanup_temp, parse_params


router = APIRouter(prefix="/api/duplicate", tags=["图片重复检测"])


@router.post("/process")
async def process(
    files: list[UploadFile] = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    threshold = int(p.get("threshold", 10))

    paths = []
    file_ids = []
    try:
        hashes = []
        filenames = []
        for f in files:
            fp, fid = save_upload(f)
            paths.append(fp)
            file_ids.append(fid)
            filenames.append(f.filename or "unknown")
            img = Image.open(fp).convert("RGB")
            hashes.append(imagehash.phash(img))

        groups = []
        used = set()
        for i, j in combinations(range(len(hashes)), 2):
            if (hashes[i] - hashes[j]) <= threshold:
                if i not in used and j not in used:
                    groups.append([filenames[i], filenames[j]])
                    used.add(i)
                    used.add(j)
                elif i in used:
                    for g in groups:
                        if filenames[i] in g and filenames[j] not in g:
                            g.append(filenames[j])
                            used.add(j)

        return JSONResponse({
            "total": len(files),
            "duplicate_groups": len(groups),
            "groups": groups,
            "threshold": threshold,
        })
    finally:
        for fp in paths:
            cleanup_temp(fp)
