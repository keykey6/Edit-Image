"""45 个功能的搜索描述数据。每项: (path, title, icon, category_key, search_text)
search_text 用于语义匹配，包含功能名、关键词、使用场景。
"""

TOOLS: list[tuple[str, str, str, str, str]] = [
    # ===== 图片调整 =====
    ("/crop-rotate", "裁剪旋转", "Crop", "basic",
     "裁剪旋转 裁切图片 旋转方向 翻转镜像 按比例裁剪 自由裁剪 任意角度旋转 纠正照片方向"),
    ("/compress", "图片压缩", "FolderOpened", "basic",
     "图片压缩 减小文件体积 缩小照片大小 压缩到指定大小 调整画质 JPEG压缩 PNG压缩 WebP压缩 批量压缩"),
    ("/format-convert", "格式转换", "Switch", "basic",
     "格式转换 图片格式互转 JPG转PNG PNG转JPG WebP转换 BMP转换 批量转换格式 改变图片类型"),
    ("/rounded-border", "圆角边框", "FullScreen", "basic",
     "圆角边框 圆角图片 给图片加边框 圆角矩形 四角圆角 自定义圆角大小 白色边框"),
    ("/image-info", "图片信息", "InfoFilled", "basic",
     "图片信息 查看图片属性 分辨率尺寸 文件大小 EXIF信息 拍摄参数 相机型号 GPS位置信息"),
    ("/dpi", "DPI设置", "ScaleToOriginal", "basic",
     "DPI设置 修改DPI 打印分辨率 300dpi 72dpi 修改分辨率 图片清晰度 打印图片"),

    # ===== 颜色与光影 =====
    ("/color-filter", "调色滤镜", "MagicStick", "color",
     "调色滤镜 滤镜效果 黑白滤镜 复古滤镜 暖色调 冷色调 日系色调 电影色调 色彩调节 照片调色 美化图片颜色"),
    ("/curve", "曲线调色", "TrendCharts", "color",
     "曲线调色 曲线工具 调整明暗 对比度调整 RGB曲线 色调曲线 专业调色 亮度对比度 高光阴影调整"),
    ("/hsl", "HSL调色", "Coin", "color",
     "HSL调色 色相饱和度 明度调整 改变色调 增加饱和度 降低亮度 色彩微调 颜色调整"),
    ("/dehaze", "去雾提亮", "Sunny", "color",
     "去雾提亮 去雾霾 照片去灰 增加对比度 雾天照片处理 清晰化 通透感 照片去朦胧"),
    ("/histogram", "图片直方图", "Histogram", "color",
     "图片直方图 查看直方图 曝光分析 RGB直方图 亮度分布 色彩分布 通道直方图 判断过曝欠曝"),
    ("/color-analysis", "色彩分析", "DataAnalysis", "color",
     "色彩分析 提取主色调 配色分析 颜色统计 调色板 色板提取 分析图片颜色 主题色识别"),

    # ===== 艺术效果 =====
    ("/sketch-effect", "素描漫画", "Brush", "effects",
     "素描漫画 照片变素描 铅笔素描 漫画效果 卡通化 手绘风格 线稿效果 艺术化 照片转手绘"),
    ("/shadow", "阴影倒影", "Picture", "effects",
     "阴影倒影 添加阴影 倒影效果 镜面倒影 立体阴影 产品展示 图片立体感 投影"),
    ("/perspective", "透视矫正", "Crop", "effects",
     "透视矫正 梯形校正 文档扫描矫正 图片拉直 变形校正 建筑摄影矫正 手机拍文档"),

    # ===== 人像美化 =====
    ("/id-photo", "证件照", "Camera", "portrait",
     "证件照 一寸照片 二寸照片 护照照片 签证照片 换底色 证件照制作 照片尺寸 标准证件照 免冠照片"),
    ("/remove-bg", "AI抠图", "Scissor", "portrait",
     "AI抠图 去除背景 背景消除 智能抠图 一键去背景 人物抠图 商品抠图 透明背景 把背景去掉 去掉背景"),
    ("/change-bg", "换背景", "Picture", "portrait",
     "换背景 更换背景 替换背景 照片换底 白色背景 蓝色背景 自定义背景 证件照换底色"),
    ("/face-beauty", "人像美颜", "Star", "portrait",
     "人像美颜 美颜 磨皮美白 瘦脸 自拍美化 皮肤美白 人像美容 脸部修饰 祛痘 光滑皮肤"),
    ("/photo-restore", "老照片修复", "Timer", "portrait",
     "老照片修复 照片修复 去除划痕 旧照片翻新 去噪点 增强清晰度 修复破损照片 老照片上色 黑白照片修复"),
    ("/suit-change", "证件照换装", "User", "portrait",
     "证件照换装 换西装 换正装 证件照衣服 换职业装 西装证件照 正装照 换衣服"),

    # ===== 安全与隐私 =====
    ("/watermark-add", "水印添加", "Edit", "privacy",
     "水印添加 加水印 图片水印 文字水印 图片水印 版权保护 防盗图 签名水印 批量加水印"),
    ("/watermark-remove", "水印去除", "Delete", "privacy",
     "水印去除 去水印 消除水印 删除水印 移除水印 去除LOGO 去掉水印 除水印"),
    ("/blur-mosaic", "模糊打码", "Hide", "privacy",
     "模糊打码 马赛克 打码 模糊人脸 遮挡敏感信息 车牌打码 高斯模糊 身份信息打码 隐私保护"),
    ("/privacy-erase", "隐私擦除", "Remove", "privacy",
     "隐私擦除 删除EXIF 清除图片信息 去除拍摄数据 隐私保护 抹除GPS位置 清除相机信息"),
    ("/encrypt", "图片加密", "Lock", "privacy",
     "图片加密 照片加密 密码保护 隐私照片 文件加密 AES加密 图片加锁 加密图片"),

    # ===== 拼接与布局 =====
    ("/photo-collage", "拼图", "Grid", "layout",
     "拼图 照片拼接 图片拼接 多图合成 拼图模板 网格拼图 组合图片 把多张拼一起"),
    ("/grid-split", "切图", "Operation", "layout",
     "切图 图片切割 九宫格 均匀分割 切分成多张 图片切片 均分图片 大图切小图"),
    ("/long-stitch", "长图拼接", "Connection", "layout",
     "长图拼接 长截图 聊天记录拼接 多张图拼成一张 纵向拼接 横向拼接 长图制作 滚动截图拼接"),
    ("/social-media", "社交媒体配图", "Share", "layout",
     "社交媒体配图 朋友圈裁剪 封面图 头像裁剪 各平台尺寸 小红书配图 抖音封面 社交网络图片裁剪"),

    # ===== 格式转换 =====
    ("/super-res", "分辨率放大", "ZoomIn", "convert",
     "分辨率放大 提高分辨率 图片放大 增加像素 放大清晰度 图片无损放大 超分辨率 图片变清晰"),
    ("/to-pdf", "图片转PDF", "Document", "convert",
     "图片转PDF 图片合并PDF 多图转一个PDF PDF导出 图片转文档 生成PDF文件 照片转PDF"),
    ("/to-ico", "图片转ICO", "Star", "convert",
     "图片转ICO 制作图标 网站图标 应用图标 图标制作 favicon 小图标 多尺寸图标"),

    # ===== 生成与识别 =====
    ("/qrcode-gen", "二维码生成", "Postcard", "generate",
     "二维码生成 制作二维码 生成二维码 URL二维码 文本二维码 WiFi二维码 收款码 名片二维码"),
    ("/qr-decode", "二维码解码", "View", "generate",
     "二维码解码 识别二维码 扫描二维码 读取二维码内容 解析二维码 扫码 翻译二维码"),
    ("/barcode", "条形码生成", "Tickets", "generate",
     "条形码生成 条形码 商品条码 ISBN条码 条码制作 生成条码 商品编码"),
    ("/text-to-image", "文字转图片", "EditPen", "generate",
     "文字转图片 文本生成图片 文字排版 生成文字海报 长文截图 文字卡片 名言卡片 文字图片化"),
    ("/meme", "表情包制作", "ChatLineSquare", "generate",
     "表情包制作 搞笑图片 配文字表情包 做表情包 梗图 表情包DIY 给图片加搞笑文字 制作表情"),

    # ===== 智能分析 =====
    ("/similarity", "相似度对比", "Link", "analysis",
     "相似度对比 图片相似度 比较两张图 找不同 对比差异 图片比对 两张图是否相同 图片查重"),
    ("/duplicate", "重复检测", "CopyDocument", "analysis",
     "重复检测 查找重复图片 批量查重 相似图片查找 找出重复 去重 找相同图片 清除重复照片"),
    ("/quality-score", "质量评分", "Medal", "analysis",
     "质量评分 图片质量 清晰度评分 画质评分 照片质量评估 模糊检测 噪点评分 图片好坏评分"),
    ("/color-picker", "取色器", "Brush", "analysis",
     "取色器 颜色提取 取色 吸管工具 像素颜色 区域颜色 获取颜色值 HEX RGB 色号"),

    # ===== 批量与预设 =====
    ("/batch-process", "批量处理", "List", "batch",
     "批量处理 批量编辑 批量调色 批量滤镜 批量加水印 批量裁切 一键处理多张 自动化处理"),
    ("/batch-rename", "批量重命名", "Sort", "batch",
     "批量重命名 批量改名 重命名照片 序号命名 日期命名 文件批量改名 统一命名 批量文件重命名"),
    ("/batch-resize", "批量改尺寸", "Odometer", "batch",
     "批量改尺寸 批量调整大小 统一尺寸 批量缩放 批量改分辨率 批量缩小 等比缩放多张图片"),
    ("/preset-save", "处理预设", "Collection", "batch",
     "处理预设 预设管理 保存处理方案 快捷处理 收藏操作 常用操作 方案复用 一键套用预设"),
]

# 分类名映射（用于前端展示）
CATEGORY_NAMES: dict[str, str] = {
    "basic": "图片调整",
    "color": "颜色与光影",
    "effects": "艺术效果",
    "portrait": "人像美化",
    "privacy": "安全与隐私",
    "layout": "拼接与布局",
    "convert": "格式工具",
    "generate": "生成与识别",
    "analysis": "智能分析",
    "batch": "批量操作",
}
