import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from config import UPLOAD_DIR
from services.image_utils import save_upload, load_image, cleanup_temp, parse_params


def _out_path(file_id: str) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}_out.png")


router = APIRouter(prefix="/api/photo-collage", tags=["拼图"])


@router.post("/process")
async def process(
    files: list[UploadFile] = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    rows = max(1, int(p.get("rows", 2)))
    cols = max(1, int(p.get("cols", 2)))
    spacing = max(0, int(p.get("spacing", 8)))
    bg_color = p.get("bg_color", "#ffffff")
    max_width = int(p.get("max_width", 1200))

    paths = []
    file_ids = []
    try:
        for f in files[:rows * cols]:
            fp, fid = save_upload(f)
            paths.append(fp)
            file_ids.append(fid)

        images = [load_image(fp) for fp in paths]

        cell_w = max(img.width for img in images)
        cell_h = max(img.height for img in images)

        canvas_w = cell_w * cols + spacing * (cols + 1)
        canvas_h = cell_h * rows + spacing * (rows + 1)

        if canvas_w > max_width:
            ratio = max_width / canvas_w
            cell_w = int(cell_w * ratio)
            cell_h = int(cell_h * ratio)
            canvas_w = max_width
            canvas_h = cell_h * rows + spacing * (rows + 1)

        canvas = Image.new("RGB", (canvas_w, canvas_h), bg_color)

        for i, img in enumerate(images):
            if i >= rows * cols:
                break
            r, c = i // cols, i % cols
            resized = img.copy()
            resized.thumbnail((cell_w, cell_h), Image.LANCZOS)
            ox = c * (cell_w + spacing) + spacing + (cell_w - resized.width) // 2
            oy = r * (cell_h + spacing) + spacing + (cell_h - resized.height) // 2
            canvas.paste(resized, (ox, oy))

        op = _out_path(file_ids[0])
        canvas.save(op, "PNG")
        return FileResponse(op, media_type="image/png", filename="collage.png")
    finally:
        for fp in paths:
            cleanup_temp(fp)
