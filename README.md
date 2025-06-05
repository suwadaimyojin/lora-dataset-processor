# LoRA数据集图像智能裁剪工具 (Lora Dataset Image Processor)

本项目旨在提供一个便捷的Web界面工具，用于批量智能裁剪图片，以便生成适用于训练LoRA模型的高质量数据集。它结合了可选的后端人物检测API和前端的 `smartcrop.js` 库，实现对图片中**人物核心区域的精确识别和智能构图优化**，并能**自适应处理图片分辨率**，确保输出符合特定尺寸约束（如任意一边不超过1024像素，且此约束可动态调整）。

[![工具界面截图](https://csv-cdn-1314342128.cos.ap-guangzhou.myqcloud.com/lora_image_processor_project.PNG)]


## ✨ 主要功能与核心优势 (相较于通用工具如 Birme.net)

*   **🎯 专为LoRA训练优化的人物核心区域智能裁剪：**
    *   **区别点：** 不同于 Birme.net 主要依赖 `smartcrop.js` 进行通用内容感知裁剪，本工具通过**可选的后端API（例如基于YOLOv8的`imgutils`服务）优先检测图像中的人物主体**。
    *   **优势：** 检测到的人物区域将作为 `smartcrop.js` 的**强力指导 (`boost`区域)**，确保裁剪的**核心始终是人物**，即使在复杂的背景或构图中也能精准定位。
    *   `smartcrop.js` 随后在**人物核心区域附近进行智能构图优化**，寻找最佳的裁剪边界，旨在包含适量的上下文信息，而非仅仅框出人物。

*   **🖼️ 自适应分辨率处理与可配置尺寸约束：**
    *   **区别点：** 本工具在最终输出时，会严格按照“任意一边不超过用户设定的最大值（默认为1024像素），超出则按比例缩放”的策略进行处理。
    *   **优势：** 用户可以**动态调整这个最大边长约束**，工具会自动重新计算并应用到所有图片。这对于需要统一数据集尺寸规范的LoRA训练尤为重要，同时保证了图片不会因过度放大而失真，或因过度缩小而丢失细节。Birme.net 虽然也提供尺寸调整，但本工具的策略更侧重于在保持人物主体和构图的前提下自适应缩放。


## 🎯 项目目标

为LoRA模型训练解决手动裁剪费时费力的问题，并帮助生成构图更合理、更能突出主体的训练数据集，从而提升LoRA模型的训练效果。

## 🚀 技术栈

*   **前端：**
    *   HTML5, CSS3, JavaScript (ES6+)
    *   [smartcrop.js](https://github.com/jwagner/smartcrop.js/): 核心智能裁剪库。
*   **后端 (用于人物检测API)：**
    *   Python
    *   [imgutils](https://github.com/deepghs/imgutils): (示例中用于调用YOLOv8进行人物检测的库)

## 🛠️ 如何使用与部署

### 1. 前端部分

*   在本地直接用浏览器打开 `Index.html` 文件运行。

### 2. 后端API 

*   如果你希望使用人物检测功能来指导 `smartcrop.js`：
    *   你需要一个后端服务，该服务接收图片上传，使用如 `imgutils` (YOLOv8) 或其他检测模型进行人物检测，并返回边界框坐标。

### 3. 基本使用流程

1.  运行api_server下的的app.py
2.  运行web_ui下的 `Index.html` 页面。
3.  通过拖拽或点击上传区域选择一批图片。
4.  图片将以瓦片形式显示，并自动应用初始的智能裁剪预览。
5.  点击并拖动每个图片瓦片上的红色虚线框，手动微调裁剪区域。
6.  完成设置和调整后，点击“全部保存为 ZIP”或“逐个保存文件”来获取处理后的图片。

##  配置与定制

*   **后端API URL：** 在前端JavaScript代码中修改 `getBoostRegionsForFile` 函数内的API请求地址。
*   **`smartcrop.js` 参数：** 在 `updateTilePreview` 函数中，你可以调整传递给 `smartcrop.crop()` 的 `options` 对象，例如：
    *   `minScale`: 控制裁剪的最小缩放程度。
    *   传递给 `options.width` 和 `options.height` 的分析用宽高：影响 `smartcrop.js` 分析时的“视窗”和宽高比偏好。
    *   `ruleOfThirds`: 是否启用三分法规则进行评分。
*   **最大输出边长：** 在JavaScript代码顶部或UI中设置 `MAX_OUTPUT_DIM_CONFIG` 的值。
*   **默认扩展因子 (用于扩充背景)：** 在 `updateTilePreview` 函数中，当使用API返回的 `boostRegionsFromAPI` 时，调整 `analysisWidth` 和 `analysisHeight` 的计算方式，以控制 `smartcrop.js` 尝试包含多少背景上下文。



##  致谢

*   [smartcrop.js](https://github.com/jwagner/smartcrop.js/)
*   [imgutils](https://github.com/deepghs/imgutils)

## 📄 许可证

例如: 本项目采用 [MIT许可证](./LICENSE)。
