import math
import os
import sys

import numpy as np

from src.exceptions import BadRequestError
from src.utils.image_utils import base64_to_bgr

MODEL_PACK = "buffalo_l"
# Ngưỡng cosine similarity (ArcFace buffalo_l); khớp khi similarity >= threshold
DEFAULT_THRESHOLD = 0.4


def _project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _insightface_root() -> str:
    if getattr(sys, "frozen", False):
        return os.path.join(getattr(sys, "_MEIPASS", ""), "insightface")
    env = os.environ.get("INSIGHTFACE_HOME")
    if env:
        return os.path.expanduser(env)
    return _project_root()


class FaceCompareService:
    DEFAULT_MODEL = "ArcFace"
    DEFAULT_DETECTOR = "insightface"
    DEFAULT_METRIC = "cosine"

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        detector_backend: str = DEFAULT_DETECTOR,
        distance_metric: str = DEFAULT_METRIC,
        threshold: float = DEFAULT_THRESHOLD,
    ):
        self._model_name = model_name
        self._detector_backend = detector_backend
        self._distance_metric = distance_metric
        self._threshold = float(threshold)
        self._app = self._load_app()

    def _load_app(self):
        from insightface.app import FaceAnalysis

        root = _insightface_root()
        app = FaceAnalysis(
            name=MODEL_PACK,
            root=root,
            allowed_modules=["detection", "recognition"],
            providers=["CPUExecutionProvider"],
        )
        app.prepare(ctx_id=-1, det_size=(640, 640))
        return app

    def _embedding(self, image: np.ndarray, field_name: str) -> np.ndarray:
        faces = self._app.get(image)
        if not faces:
            raise BadRequestError(f"Không phát hiện được khuôn mặt trong ảnh khi so sánh.")
        face = max(
            faces,
            key=lambda f: float((f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])),
        )
        emb = face.normed_embedding
        if emb is None:
            raise BadRequestError(f"Không trích xuất được embedding từ {field_name}.")
        return np.asarray(emb, dtype=np.float32).ravel()

    def compare_images(self, image1: str | None, image2: str | None) -> dict:
        if image1 is None or image2 is None:
            raise BadRequestError(
                "Cần gửi ảnh (chuỗi base64). "
                "JSON: Content-Type application/json, hoặc form field ảnh1/ảnh2."
            )
        if not isinstance(image1, str) or not isinstance(image2, str):
            raise BadRequestError("Ảnh phải là chuỗi base64")

        img1 = base64_to_bgr(image1, "image1")
        img2 = base64_to_bgr(image2, "image2")

        emb1 = self._embedding(img1, "image1")
        emb2 = self._embedding(img2, "image2")

        similarity = float(np.clip(np.dot(emb1, emb2), 0.0, 1.0))
        distance = round(1.0 - similarity, 4)
        verified = similarity >= self._threshold

        return {
            "match_percent": to_match_percent(similarity),
            "similarity": round(similarity, 4),
            "is_match": verified,
            "threshold": self._threshold,
            "distance": distance,
        }


def distance_to_similarity(
    distance: float,
    metric: str = "cosine",
    threshold: float | None = None,
) -> float:
    """Đảo distance về similarity (0–1)."""
    d = float(distance)

    if metric == "cosine":
        return round(max(0.0, min(1.0, 1.0 - d)), 4)

    if metric == "angular":
        return round(max(0.0, min(1.0, math.cos(d * math.pi))), 4)

    if metric in ("euclidean", "euclidean_l2") and threshold and threshold > 0:
        return round(max(0.0, min(1.0, 1.0 - d / threshold)), 4)

    return round(max(0.0, min(1.0, 1.0 - d)), 4)


def to_match_percent(similarity: float) -> float:
    """Chuyển similarity (0–1) sang phần trăm khớp (0–100)."""
    return round(max(0.0, min(1.0, similarity)) * 100.0, 2)
