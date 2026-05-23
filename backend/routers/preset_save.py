import os
import json
import uuid
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from config import UPLOAD_DIR
from services.image_utils import parse_params


PRESETS_FILE = os.path.join(UPLOAD_DIR, "presets.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/api/preset-save", tags=["处理预设"])


def _load_presets() -> list:
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_presets(presets: list):
    with open(PRESETS_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)


@router.get("/list")
async def list_presets():
    presets = _load_presets()
    return JSONResponse({"presets": presets})


@router.post("/save")
async def save_preset(
    params: str | None = Form(None),
):
    p = parse_params(params)
    name = p.get("name", "未命名预设")
    module = p.get("module", "")
    preset_params = p.get("params", {})

    presets = _load_presets()
    pid = uuid.uuid4().hex[:8]
    presets.append({
        "id": pid,
        "name": name,
        "module": module,
        "params": preset_params,
    })
    _save_presets(presets)
    return JSONResponse({"id": pid, "message": "预设已保存"})


@router.post("/delete")
async def delete_preset(
    params: str | None = Form(None),
):
    p = parse_params(params)
    pid = p.get("id", "")
    presets = _load_presets()
    presets = [pr for pr in presets if pr.get("id") != pid]
    _save_presets(presets)
    return JSONResponse({"message": "预设已删除"})
