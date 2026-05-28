import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'

export interface RouteMeta {
  title: string
  icon: string
  category: string
}

export const CATEGORIES: Record<string, string> = {
  basic: '图片调整',
  color: '颜色与光影',
  effects: '艺术效果',
  portrait: '人像美化',
  privacy: '安全与隐私',
  layout: '拼接与布局',
  convert: '格式工具',
  generate: '生成与识别',
  analysis: '智能分析',
  batch: '批量操作',
}

export const DESCRIPTIONS: Record<string, string> = {
  basic: '裁剪、压缩、格式转换、DPI设置等基础图像操作',
  color: '滤镜调色、曲线、HSL、直方图、色彩分析',
  effects: '素描、漫画、阴影倒影、透视矫正',
  portrait: '证件照、AI抠图、换背景、美颜、修复、换装',
  privacy: '水印添加与去除、模糊打码、隐私擦除、图片加密',
  layout: '拼图、切图、长图拼接、社交媒体配图裁剪',
  convert: '分辨率放大、图片转PDF、图片转ICO图标',
  generate: '二维码生成与解码、条形码、文字转图、表情包',
  analysis: '相似度对比、重复检测、质量评分、取色器',
  batch: '批量处理、批量重命名、批量改尺寸、预设管理',
}

export const ROUTES = [
  // ===== 基础编辑 =====
  { path: '/crop-rotate', name: 'CropRotate', component: () => import('@/views/CropRotate.vue'), meta: { title: '裁剪旋转', icon: 'Crop', category: 'basic' } },
  { path: '/compress', name: 'Compress', component: () => import('@/views/Compress.vue'), meta: { title: '图片压缩', icon: 'FolderOpened', category: 'basic' } },
  { path: '/format-convert', name: 'FormatConvert', component: () => import('@/views/FormatConvert.vue'), meta: { title: '格式转换', icon: 'Switch', category: 'basic' } },
  { path: '/rounded-border', name: 'RoundedBorder', component: () => import('@/views/RoundedBorder.vue'), meta: { title: '圆角边框', icon: 'FullScreen', category: 'basic' } },
  { path: '/image-info', name: 'ImageInfo', component: () => import('@/views/ImageInfo.vue'), meta: { title: '图片信息', icon: 'InfoFilled', category: 'basic' } },
  { path: '/dpi', name: 'Dpi', component: () => import('@/views/Dpi.vue'), meta: { title: 'DPI设置', icon: 'ScaleToOriginal', category: 'basic' } },

  // ===== 调色与增强 =====
  { path: '/color-filter', name: 'ColorFilter', component: () => import('@/views/ColorFilter.vue'), meta: { title: '调色滤镜', icon: 'MagicStick', category: 'color' } },
  { path: '/curve', name: 'Curve', component: () => import('@/views/Curve.vue'), meta: { title: '曲线调色', icon: 'TrendCharts', category: 'color' } },
  { path: '/hsl', name: 'Hsl', component: () => import('@/views/Hsl.vue'), meta: { title: 'HSL调色', icon: 'Coin', category: 'color' } },
  { path: '/dehaze', name: 'Dehaze', component: () => import('@/views/Dehaze.vue'), meta: { title: '去雾提亮', icon: 'Sunny', category: 'color' } },
  { path: '/histogram', name: 'Histogram', component: () => import('@/views/Histogram.vue'), meta: { title: '图片直方图', icon: 'Histogram', category: 'color' } },
  { path: '/color-analysis', name: 'ColorAnalysis', component: () => import('@/views/ColorAnalysis.vue'), meta: { title: '色彩分析', icon: 'DataAnalysis', category: 'color' } },

  // ===== 滤镜特效 =====
  { path: '/sketch-effect', name: 'SketchEffect', component: () => import('@/views/SketchEffect.vue'), meta: { title: '素描漫画', icon: 'Brush', category: 'effects' } },
  { path: '/shadow', name: 'Shadow', component: () => import('@/views/Shadow.vue'), meta: { title: '阴影倒影', icon: 'Picture', category: 'effects' } },
  { path: '/perspective', name: 'Perspective', component: () => import('@/views/Perspective.vue'), meta: { title: '透视矫正', icon: 'Crop', category: 'effects' } },

  // ===== 人像处理 =====
  { path: '/id-photo', name: 'IdPhoto', component: () => import('@/views/IdPhoto.vue'), meta: { title: '证件照', icon: 'Camera', category: 'portrait' } },
  { path: '/remove-bg', name: 'RemoveBg', component: () => import('@/views/RemoveBg.vue'), meta: { title: 'AI抠图', icon: 'Scissor', category: 'portrait' } },
  { path: '/change-bg', name: 'ChangeBg', component: () => import('@/views/ChangeBg.vue'), meta: { title: '换背景', icon: 'Picture', category: 'portrait' } },
  { path: '/face-beauty', name: 'FaceBeauty', component: () => import('@/views/FaceBeauty.vue'), meta: { title: '人像美颜', icon: 'Star', category: 'portrait' } },
  { path: '/photo-restore', name: 'PhotoRestore', component: () => import('@/views/PhotoRestore.vue'), meta: { title: '老照片修复', icon: 'Timer', category: 'portrait' } },
  { path: '/suit-change', name: 'SuitChange', component: () => import('@/views/SuitChange.vue'), meta: { title: '证件照换装', icon: 'User', category: 'portrait' } },

  // ===== 水印与隐私 =====
  { path: '/watermark-add', name: 'WatermarkAdd', component: () => import('@/views/WatermarkAdd.vue'), meta: { title: '水印添加', icon: 'Edit', category: 'privacy' } },
  { path: '/watermark-remove', name: 'WatermarkRemove', component: () => import('@/views/WatermarkRemove.vue'), meta: { title: '水印去除', icon: 'Delete', category: 'privacy' } },
  { path: '/blur-mosaic', name: 'BlurMosaic', component: () => import('@/views/BlurMosaic.vue'), meta: { title: '模糊打码', icon: 'Hide', category: 'privacy' } },
  { path: '/privacy-erase', name: 'PrivacyErase', component: () => import('@/views/PrivacyErase.vue'), meta: { title: '隐私擦除', icon: 'Remove', category: 'privacy' } },
  { path: '/encrypt', name: 'Encrypt', component: () => import('@/views/Encrypt.vue'), meta: { title: '图片加密', icon: 'Lock', category: 'privacy' } },

  // ===== 拼图排版 =====
  { path: '/photo-collage', name: 'PhotoCollage', component: () => import('@/views/PhotoCollage.vue'), meta: { title: '拼图', icon: 'Grid', category: 'layout' } },
  { path: '/grid-split', name: 'GridSplit', component: () => import('@/views/GridSplit.vue'), meta: { title: '切图', icon: 'Operation', category: 'layout' } },
  { path: '/long-stitch', name: 'LongStitch', component: () => import('@/views/LongStitch.vue'), meta: { title: '长图拼接', icon: 'Connection', category: 'layout' } },
  { path: '/social-media', name: 'SocialMedia', component: () => import('@/views/SocialMedia.vue'), meta: { title: '社交媒体配图', icon: 'Share', category: 'layout' } },

  // ===== 格式转换 =====
  { path: '/super-res', name: 'SuperRes', component: () => import('@/views/SuperRes.vue'), meta: { title: '分辨率放大', icon: 'ZoomIn', category: 'convert' } },
  { path: '/to-pdf', name: 'ToPdf', component: () => import('@/views/ToPdf.vue'), meta: { title: '图片转PDF', icon: 'Document', category: 'convert' } },
  { path: '/to-ico', name: 'ToIco', component: () => import('@/views/ToIco.vue'), meta: { title: '图片转ICO', icon: 'Star', category: 'convert' } },

  // ===== 生成与解码 =====
  { path: '/qrcode-gen', name: 'QrcodeGen', component: () => import('@/views/QrcodeGen.vue'), meta: { title: '二维码生成', icon: 'Postcard', category: 'generate' } },
  { path: '/qr-decode', name: 'QrDecode', component: () => import('@/views/QrDecode.vue'), meta: { title: '二维码解码', icon: 'View', category: 'generate' } },
  { path: '/barcode', name: 'Barcode', component: () => import('@/views/Barcode.vue'), meta: { title: '条形码生成', icon: 'Tickets', category: 'generate' } },
  { path: '/text-to-image', name: 'TextToImage', component: () => import('@/views/TextToImage.vue'), meta: { title: '文字转图片', icon: 'EditPen', category: 'generate' } },
  { path: '/meme', name: 'Meme', component: () => import('@/views/Meme.vue'), meta: { title: '表情包制作', icon: 'ChatLineSquare', category: 'generate' } },

  // ===== 智能分析 =====
  { path: '/similarity', name: 'Similarity', component: () => import('@/views/Similarity.vue'), meta: { title: '相似度对比', icon: 'Link', category: 'analysis' } },
  { path: '/duplicate', name: 'Duplicate', component: () => import('@/views/Duplicate.vue'), meta: { title: '重复检测', icon: 'CopyDocument', category: 'analysis' } },
  { path: '/quality-score', name: 'QualityScore', component: () => import('@/views/QualityScore.vue'), meta: { title: '质量评分', icon: 'Medal', category: 'analysis' } },
  { path: '/color-picker', name: 'ColorPicker', component: () => import('@/views/ColorPickerView.vue'), meta: { title: '取色器', icon: 'Brush', category: 'analysis' } },

  // ===== 批量与预设 =====
  { path: '/batch-process', name: 'BatchProcess', component: () => import('@/views/BatchProcess.vue'), meta: { title: '批量处理', icon: 'List', category: 'batch' } },
  { path: '/batch-rename', name: 'BatchRename', component: () => import('@/views/BatchRename.vue'), meta: { title: '批量重命名', icon: 'Sort', category: 'batch' } },
  { path: '/batch-resize', name: 'BatchResize', component: () => import('@/views/BatchResize.vue'), meta: { title: '批量改尺寸', icon: 'Odometer', category: 'batch' } },
  { path: '/preset-save', name: 'PresetSave', component: () => import('@/views/PresetSave.vue'), meta: { title: '处理预设', icon: 'Collection', category: 'batch' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: HomePage, meta: { title: '首页', icon: 'HomeFilled', category: '' } },
    { path: '/all-tools', name: 'AllTools', component: () => import('@/views/AllTools.vue'), meta: { title: '全部工具', icon: 'Grid', category: '' } },
    ...ROUTES,
  ],
})

export default router
