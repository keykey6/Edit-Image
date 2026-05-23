import os
import struct
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from config import UPLOAD_DIR
from services.image_utils import save_upload, cleanup_temp, parse_params


def _out_path(file_id: str, suffix: str = "") -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return os.path.join(UPLOAD_DIR, f"{file_id}{suffix}")


router = APIRouter(prefix="/api/encrypt", tags=["图片加密"])


def _derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


@router.post("/process")
async def process(
    file: UploadFile = File(...),
    params: str | None = Form(None),
):
    p = parse_params(params)
    password = p.get("password", "123456")
    action = p.get("action", "encrypt")  # encrypt / decrypt

    filepath, file_id = save_upload(file)
    try:
        with open(filepath, "rb") as f:
            data = f.read()

        key = _derive_key(password)

        if action == "encrypt":
            iv = os.urandom(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            # 前4字节存原文件长度，方便解密时去padding
            header = struct.pack(">I", len(data))
            encrypted = cipher.encrypt(pad(header + data, AES.block_size))
            payload = iv + encrypted
        else:
            iv = data[:16]
            encrypted = data[16:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
            orig_len = struct.unpack(">I", decrypted[:4])[0]
            payload = decrypted[4:4 + orig_len]

        suffix = ".enc" if action == "encrypt" else "_decrypted.png"
        op = _out_path(file_id, suffix)
        with open(op, "wb") as f:
            f.write(payload)

        media_type = "application/octet-stream" if action == "encrypt" else "image/png"
        filename = "encrypted.bin" if action == "encrypt" else "decrypted.png"
        return FileResponse(op, media_type=media_type, filename=filename)
    finally:
        cleanup_temp(filepath)
