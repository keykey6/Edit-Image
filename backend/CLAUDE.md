# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

超级全能图像工具箱 — a local image processing toolbox with 45 functional modules. Backend is FastAPI (:9000), frontend is Vue3 + Element Plus (:5173). All features are pure Python — no cloud API dependencies.

Full architecture: [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).

## Dev commands

```bash
# Backend (backend/)
cd backend
uv run uvicorn main:app --host 0.0.0.0 --port 9000 --reload

# Frontend (frontend/)
cd frontend
pnpm dev                          # dev server with hot reload
pnpm build                        # type-check + production build

# Install new dependency
cd backend && uv add <pkg>
cd frontend && pnpm add <pkg>
```

## API pattern — every module follows this

```
POST /api/{module}/process
Content-Type: multipart/form-data
  file:  <binary>         — single image
  files: <binary>...      — multiple images (batch ops)
  params: '{"key":"val"}' — JSON string
```

Response: `FileResponse` (image/zip) or `JSONResponse` (analysis data).

## Critical patterns

### Backend router template

Every router in `routers/` follows this exact pattern:

```python
router = APIRouter(prefix="/api/module-name", tags=["中文标签"])

@router.post("/process")
async def process(
    file: UploadFile = File(...),          # or files: list[UploadFile]
    params: str | None = Form(None),
):
    p = parse_params(params)
    fpath, file_id = save_upload(file)
    try:
        img = Image.open(fpath).convert("RGB")
        # ... process ...
        out = save_image(result, file_id, "png")
        return FileResponse(out, media_type="image/png")
    finally:
        cleanup_temp(fpath)
```

Register in `main.py`: import + add to `routers` list.

### Chinese path handling — MUST follow this

- `cv2.imwrite()` fails on paths with Chinese characters → use `Image.fromarray(arr).save(path)`
- `cv2.imread()` can fail on Chinese paths → use PIL `Image.open()` then convert to numpy if needed
- `cv2.CascadeClassifier()` can't load from Chinese paths → copy cascade file to `tempfile.gettempdir()` first

### Image save format

Always use `save_image()` from `services/image_utils.py` — it handles JPEG quality, WebP settings, format normalization. For OpenCV numpy arrays: `Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)).save(path)`.

### Frontend ToolPage pattern (~35 views)

```vue
<template>
  <ToolPage module="module-name" :params="params">
    <template #params>
      <!-- custom controls here -->
    </template>
  </ToolPage>
</template>
```

ToolPage handles: upload → loading → error → before/after compare → download. Only write a custom view when you need: multi-file input, dual-file input, JSON display, or a multi-step flow.

### Frontend views that bypass ToolPage

These ~10 views manage their own state: `IdPhoto`, `ChangeBg`, `PhotoCollage`, `GridSplit`, `BatchProcess`, `LongStitch`, `ToPdf`, `BatchRename`, `BatchResize`, `Similarity`, `Duplicate`, `PresetSave`, `QrDecode`, `ColorPickerView`, `ColorAnalysis`, `QualityScore`.

### Route registration

All 45 routes in `src/router/index.ts`. Each has `meta: { title, icon, category }`. `category` maps to sidebar grouping via `CATEGORIES` and `DESCRIPTIONS` constants. Add new routes to the correct category.

### Numpy int64 → JSON

`imagehash` subtraction returns `numpy.int64` which `json.dumps` rejects. Always wrap with `int()`: `diff = int(h1 - h2)`.

## Utility functions (`services/image_utils.py`)

| Function | Purpose |
|----------|---------|
| `parse_params(str)` | Parse JSON params from form, returns dict |
| `save_upload(file)` | Write upload to disk, returns (path, file_id) |
| `load_image(path)` | PIL `Image.open().convert("RGB")` |
| `save_image(img, file_id, fmt)` | Save PIL image, returns output path |
| `cleanup_temp(path)` | Delete temp file if exists |

## Project config

- `config.py`: `UPLOAD_DIR`, `MAX_FILE_SIZE` (20MB), `ALLOWED_EXTENSIONS`, `CORS_ORIGINS`
- Frontend proxy: `/api` → `localhost:9000` (vite.config.ts)
- No database; presets stored in `uploads/presets.json`
