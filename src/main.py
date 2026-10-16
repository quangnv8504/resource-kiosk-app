import os

from flask import Flask, jsonify
from flask_cors import CORS

from src.api.pace_api import bp
from src.services.face_compare import FaceCompareService
from src.exceptions import register_exception_handlers


def _cors_origins() -> str | list[str]:
    raw = os.environ.get("CORS_ORIGINS", "*").strip()
    if not raw or raw == "*":
        return "*"
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def create_app() -> Flask:
    app = Flask(__name__)

    max_body_bytes = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "10")) * 1024 * 1024
    app.config["MAX_CONTENT_LENGTH"] = max_body_bytes
    # Mặc định Flask 3.1 chỉ cho mỗi field form ~500KB, không đủ cho ảnh base64
    app.config["MAX_FORM_MEMORY_SIZE"] = max_body_bytes

    CORS(app, resources={r"/*": {"origins": _cors_origins()}})
    register_exception_handlers(app)
    app.register_blueprint(bp)

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "stack": "insightface-onnx",
                "model": FaceCompareService.DEFAULT_MODEL,
                "detector": FaceCompareService.DEFAULT_DETECTOR,
            }
        )

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8001, debug=True)
