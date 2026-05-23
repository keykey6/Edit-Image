from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from PIL import Image
from services.image_utils import save_upload, load_image, save_image, cleanup_temp, parse_params

router = APIRouter(prefix="/api/crop-rotate", tags=["裁剪旋转"])


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    action = p.get("action", "crop")
    filepath, file_id = save_upload(file)
    try:
        img = load_image(filepath)
        w, h = img.size

        if action == "crop":
            x = max(0, int(p.get("x", 0)))
            y = max(0, int(p.get("y", 0)))
            cw = min(w - x, int(p.get("width", w)))
            ch = min(h - y, int(p.get("height", h)))
            img = img.crop((x, y, x + cw, y + ch))

        elif action == "rotate":
            angle = float(p.get("angle", 0))
            expand = bool(p.get("expand", True))
            img = img.rotate(angle, expand=expand)

        elif action == "flip":
            direction = p.get("direction", "horizontal")
            if direction == "horizontal":
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif direction == "vertical":
                img = img.transpose(Image.FLIP_TOP_BOTTOM)

        out_path = save_image(img, file_id)
        return FileResponse(out_path, media_type="image/png", filename="result.png")
    finally:
        cleanup_temp(filepath)
