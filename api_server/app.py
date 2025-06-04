from flask import Flask, request, jsonify
from flask_cors import CORS
from imgutils.detect import detect_person  # 核心检测库
import io  # 用于处理上传的文件流

app = Flask(__name__)
# 允许所有来源的跨域请求，生产环境中应配置得更严格
# 如果你的前端和这个API部署在同一个域下，或者你通过代理访问，可能不需要这么宽松的CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/detect/person_regions", methods=["POST"])
def detect_person_regions_api():
    if "image" not in request.files:
        return jsonify({"error": '请求中未找到 "image" 文件部分'}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "没有选择文件"}), 400

    if file:  # 确保文件存在且被正确上传
        try:
            image_bytes_io = io.BytesIO(file.read())

            # 调用人物检测函数
            # 你可以根据需要调整 level, conf_threshold, iou_threshold 等参数
            # 例如: detection_results = detect_person(image_bytes_io, level='m', conf_threshold=0.35)
            detection_results = detect_person(
                image_bytes_io, conf_threshold=0.35
            )  # 示例：设置一个置信度阈值

            smartcrop_boost_regions = []
            if detection_results:
                for detection in detection_results:
                    box, label, score = detection
                    x0, y0, x1, y1 = box

                    boost_object = {
                        "x": int(x0),  # 确保是整数
                        "y": int(y0),
                        "width": int(x1 - x0),
                        "height": int(y1 - y0),
                        "weight": float(score),  # 确保是浮点数
                    }
                    smartcrop_boost_regions.append(boost_object)

            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"成功检测到 {len(smartcrop_boost_regions)} 个人物区域。",
                        "boost_regions": smartcrop_boost_regions,
                    }
                ),
                200,
            )

        except Exception as e:
            app.logger.error(
                f"人物检测 API 出错: {e}", exc_info=True
            )  # 使用 Flask logger
            return jsonify({"error": f"处理图片时发生错误: {str(e)}"}), 500

    return jsonify({"error": "上传文件处理失败"}), 400


if __name__ == "__main__":
    # 生产环境建议使用 Gunicorn 或 uWSGI 等 WSGI 服务器运行
    # 例如: gunicorn -w 4 -b 0.0.0.0:5050 person_detection_api:app
    print("Starting person detection API server on http://0.0.0.0:5050")
    app.run(debug=True, host="0.0.0.0", port=5050)  # debug=True 仅用于开发
