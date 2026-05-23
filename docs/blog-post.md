# 超级全能图像工具箱：纯本地、零付费、45个功能的开源修图神器

## 为什么要做这个项目

市面上的在线修图工具要么收费，要么上传图片到云端有隐私风险，要么功能分散需要开十几个网页。我花了一个月时间，从零搭建了一个**纯本地运行、完全免费开源**的图像处理工具箱，涵盖 45 个功能模块，一行命令即可启动。

> GitHub: [https://github.com/keykey6/Edit-Image](https://github.com/keykey6/Edit-Image)

## 一图胜千言

打开浏览器，左边深色侧栏按 10 个分类折叠导航，右边白色内容区上传→调参→处理→对比→下载，操作路径不超过三步。

整个交互围绕一个核心组件 `ToolPage` 完成：拖拽图片上传 → 调整参数滑块 → 点击"开始处理" → 在线对比原图/结果图 → 一键下载。45 个功能里有 35 个都复用这套流程，用户学一次就能用全部功能。

长得比较复杂的功能（比如证件照、批量处理、拼图、换背景），各自写了专属页面，不走通用组件。

## 10 大类 45 个功能

**图片调整** — 裁剪旋转、压缩、格式转换、圆角边框、图片信息查看、DPI 设置

**颜色与光影** — 调色滤镜、曲线调色、HSL 调色、去雾提亮、直方图、色彩分析（KMeans 聚类提取主色调）

**艺术效果** — 素描/漫画风格（Canny + 自适应阈值）、阴影倒影、透视矫正

**人像美化** — 证件照（上百种规格+人脸居中裁剪）、AI 抠图（rembg U2Net）、换背景、人像美颜（双边滤波磨皮+美白+锐化）、老照片修复（CLAHE+去噪+划痕修复）、证件照换装

**安全与隐私** — 水印添加（文字/图片/平铺）、水印去除（裁剪/模糊/inpaint）、模糊打码（人脸检测+高斯模糊）、隐私擦除（清 EXIF）、AES-256-CBC 图片加密

**拼接与布局** — 拼图、九宫格切图、长图拼接、社交媒体配图按比例裁剪

**格式工具** — 分辨率放大（Lanczos + USM 锐化）、图片转 PDF、图片转 ICO 多尺寸

**生成与识别** — 二维码生成（支持内嵌 Logo）、二维码/条形码解码、文字转图片、表情包制作

**智能分析** — 相似度对比（感知哈希 pHash/dHash/aHash/wHash）、重复图片检测、质量评分（Laplacian 方差+噪点估计）、取色器

**批量操作** — 批量处理（压缩/缩放/转格式/灰度/翻转）、批量重命名、批量改尺寸（cover/contain/stretch）、处理预设保存

## 技术架构

```
前端: Vue 3.5 + TypeScript + Vite 8 + Element Plus 2
后端: Python 3.12 + FastAPI + Uvicorn
图像: Pillow + OpenCV + rembg + imagehash + qrcode
```

选了最轻量的组合：

- **前端 7 个通用组件**支撑 46 个页面，路由懒加载，Element Plus 紫色主题 CSS 变量覆盖
- **后端统一 API**：全部模块共用 `POST /api/{module}/process`，入参 `multipart/form-data`（file + JSON params），出参 `FileResponse` 或 `JSONResponse`
- **无数据库**：预设配置存 JSON 文件，处理完的临时图片即时清理
- **零云 API 依赖**：抠图用 rembg（本地 U2Net 模型），人脸检测用 OpenCV Haar Cascade，所有图像处理纯 Python 本地完成

## 三个踩坑记录

**1. OpenCV 中文路径**

`cv2.imwrite()` 遇到中文路径直接报错，`cv2.imread()` 也一样。最后全部改成 PIL 读写：读用 `Image.open()`，写用 `Image.fromarray().save()`。

**2. mediapipe 包冲突**

PyPI 上有一个叫 `mediapipe` 的同名假包，安装后人脸检测直接崩。最后放弃 mediapipe，改用 OpenCV 自带的 Haar Cascade，效果够用。

**3. Windows 端口幽灵进程**

5173 端口经常被残留 Node 进程占用，`netstat -ano | findstr :5173` 然后 `taskkill` 是日常操作。后来把后端端口改到 9000 避开冲突。

## 一分钟跑起来

```bash
# 克隆仓库
git clone https://github.com/keykey6/Edit-Image.git
cd Edit-Image

# 启动后端（需要 Python 3.12+）
cd backend
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 9000 --reload

# 另开终端，启动前端
cd frontend
pnpm install
pnpm dev
```

浏览器打开 `http://localhost:5173` 即可使用。

## 后续计划

项目 45 个模块的功能都已实现，但还有一些明显的改进方向：

- **人脸检测升级**：Haar Cascade 精度有限，换 MTCNN 或 RetinaFace 人脸关键点检测
- **超分升级**：当前是传统插值放大，接入 Real-ESRGAN 做 AI 超分
- **老照片修复升级**：目前是传统 CV 方案，接入 GFPGAN 等 GAN 模型效果会好很多
- **国际化**：目前只有中文 UI，加 i18n 会扩大受众
- **Docker 部署**：打包成镜像方便一键部署到 NAS 或服务器

欢迎 Star、PR、提 Issue。

---

*项目地址：[https://github.com/keykey6/Edit-Image](https://github.com/keykey6/Edit-Image)*
