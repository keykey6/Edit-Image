from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import CORS_ORIGINS
from routers.crop_rotate import router as crop_rotate
from routers.compress import router as compress
from routers.format_convert import router as format_convert
from routers.rounded_border import router as rounded_border
from routers.image_info import router as image_info
from routers.remove_bg import router as remove_bg
from routers.id_photo import router as id_photo
from routers.change_bg import router as change_bg
from routers.photo_restore import router as photo_restore
from routers.face_beauty import router as face_beauty
from routers.color_filter import router as color_filter
from routers.dehaze import router as dehaze
from routers.sketch_effect import router as sketch_effect
from routers.watermark_add import router as watermark_add
from routers.watermark_remove import router as watermark_remove
from routers.photo_collage import router as photo_collage
from routers.grid_split import router as grid_split
from routers.blur_mosaic import router as blur_mosaic
from routers.suit_change import router as suit_change
from routers.batch_process import router as batch_process
from routers.super_res import router as super_res
from routers.qrcode_gen import router as qrcode_gen
from routers.curve import router as curve
from routers.hsl import router as hsl
from routers.perspective import router as perspective
from routers.shadow import router as shadow
from routers.privacy_erase import router as privacy_erase
from routers.encrypt import router as encrypt
from routers.long_stitch import router as long_stitch
from routers.social_media import router as social_media
from routers.dpi import router as dpi
from routers.to_pdf import router as to_pdf
from routers.to_ico import router as to_ico
from routers.histogram import router as histogram
from routers.color_analysis import router as color_analysis
from routers.similarity import router as similarity
from routers.duplicate import router as duplicate
from routers.quality_score import router as quality_score
from routers.qr_decode import router as qr_decode
from routers.barcode import router as barcode
from routers.text_to_image import router as text_to_image
from routers.color_picker import router as color_picker
from routers.meme import router as meme
from routers.batch_rename import router as batch_rename
from routers.batch_resize import router as batch_resize
from routers.preset_save import router as preset_save

app = FastAPI(title="超级全能图像工具箱 API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    crop_rotate, compress, format_convert, rounded_border, image_info,
    remove_bg, id_photo, change_bg, photo_restore, face_beauty,
    color_filter, dehaze, sketch_effect, watermark_add, watermark_remove,
    photo_collage, grid_split, blur_mosaic, suit_change, batch_process,
    super_res, qrcode_gen,
    curve, hsl, perspective, shadow,
    privacy_erase, encrypt,
    long_stitch, social_media,
    dpi, to_pdf, to_ico,
    histogram, color_analysis, similarity, duplicate, quality_score,
    qr_decode, barcode, text_to_image, color_picker, meme,
    batch_rename, batch_resize, preset_save,
]

for r in routers:
    app.include_router(r)


@app.get("/")
async def root():
    return {"message": "超级全能图像工具箱 API", "version": "1.0.0"}
