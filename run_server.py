"""
Entry point chạy standalone / build exe (PyInstaller onefile).
"""
import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False):
    _ROOT = os.path.dirname(sys.executable)
    os.chdir(_ROOT)

if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import onnxruntime  # noqa: F401,E402 — load trước Flask/cv2 trong bản exe
import tqdm  # noqa: F401,E402 — insightface.utils.download cần khi load model
import skimage  # noqa: F401,E402 — insightface.utils.face_align cần khi load model

from waitress import serve  # noqa: E402

from src.main import create_app  # noqa: E402


def main() -> None:
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8001"))
    app = create_app()

    print("BE Face API (InsightFace + ONNX):")
    print(f"  Health:  http://127.0.0.1:{port}/health")
    print(f"  Compare: POST http://127.0.0.1:{port}/api/v1/compare")
    print('  Body JSON: { "image1": "<base64>", "image2": "<base64>" }')
    print("Nhan Ctrl+C de dung.")

    serve(app, host=host, port=port, threads=4)


if __name__ == "__main__":
    main()
