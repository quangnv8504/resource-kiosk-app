from flask import Flask, jsonify
from flask_cors import CORS

from src.api.pace_api import bp
from src.services.face_compare import FaceCompareService
from src.exceptions import register_exception_handlers


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
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


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
