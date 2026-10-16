from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from src.exceptions.errors import AppException
from src.models.response_model import ErrorResponse


_HTTP_MESSAGES_VI = {
    400: "Yêu cầu không hợp lệ.",
    401: "Chưa xác thực.",
    403: "Không có quyền truy cập.",
    404: "Không tìm thấy đường dẫn API.",
    405: "Phương thức HTTP không được hỗ trợ cho đường dẫn này.",
    408: "Hết thời gian chờ yêu cầu.",
    413: "Dữ liệu gửi lên quá lớn.",
    415: "Định dạng dữ liệu không được hỗ trợ.",
    429: "Quá nhiều yêu cầu, vui lòng thử lại sau.",
    500: "Lỗi hệ thống, vui lòng thử lại sau.",
    502: "Lỗi cổng kết nối.",
    503: "Dịch vụ tạm thời không khả dụng.",
    504: "Hết thời gian chờ phản hồi.",
}


def _error_body(message: str) -> dict:
    return ErrorResponse(success=False, message=message).to_dict()


def register_exception_handlers(app: Flask) -> None:
    @app.errorhandler(AppException)
    def handle_app_exception(exc: AppException):
        return jsonify(_error_body(exc.message)), exc.status_code

    @app.errorhandler(ValueError)
    def handle_value_error(exc: ValueError):
        return jsonify(_error_body(str(exc))), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        code = exc.code or 500
        message = _HTTP_MESSAGES_VI.get(code, f"Lỗi HTTP {code}.")
        if code == 413:
            limit = app.config.get("MAX_CONTENT_LENGTH")
            if limit:
                message = f"Dữ liệu gửi lên quá lớn (tối đa {limit // (1024 * 1024)}MB)."
        return jsonify(_error_body(message)), code

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        app.logger.exception("Unhandled exception: %s", exc)
        return jsonify(_error_body("Lỗi hệ thống, vui lòng thử lại sau.")), 500
