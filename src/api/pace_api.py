import threading

from flask import Blueprint, jsonify, request

from src.models.response_model import CompareResponse
from src.services.face_compare import FaceCompareService

bp = Blueprint("face", __name__, url_prefix="/api/v1")
_compare_service: FaceCompareService | None = None
_compare_service_lock = threading.Lock()


def get_compare_service() -> FaceCompareService:
    global _compare_service
    if _compare_service is None:
        with _compare_service_lock:
            if _compare_service is None:
                _compare_service = FaceCompareService()
    return _compare_service


@bp.post("/compare")
def compare_faces():
    body = request.get_json(silent=True)
    if isinstance(body, dict):
        image1, image2 = body.get("image1"), body.get("image2")
    else:
        image1, image2 = None, None

    if image1 is None or image2 is None:
        image1 = request.form.get("image1")
        image2 = request.form.get("image2")

    result = get_compare_service().compare_images(image1, image2)

    return jsonify(
        CompareResponse(
            success=True,
            match_percent=result["match_percent"],
            similarity=result["similarity"],
            is_match=result["is_match"],
            threshold=result["threshold"],
            distance=result["distance"],
        ).to_dict()
    )
