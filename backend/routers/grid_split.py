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


router = APIRouter(prefix="/api/grid-split", tags=["切图"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    rows = max(1, int(p.get("rows", 2)))
    cols = max(1, int(p.get("cols", 2)))

    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)
        w, h = img.size
        cell_w, cell_h = w // cols, h // rows

        zip_path = _out_path(file_id, "_grid.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for r in range(rows):
                for c in range(cols):
                    x1, y1 = c * cell_w, r * cell_h
                    x2 = x1 + cell_w if c < cols - 1 else w
                    y2 = y1 + cell_h if r < rows - 1 else h
                    tile = img.crop((x1, y1, x2, y2))

                    tile_path = _out_path(file_id, f"_r{r}_c{c}.png")
                    tile.save(tile_path, "PNG")
                    zf.write(tile_path, f"tile_r{r}_c{c}.png")
                    os.remove(tile_path)

        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=f"grid_{rows}x{cols}.zip",
        )
    finally:
        cleanup_temp(filepath)
