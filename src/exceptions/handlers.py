from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from src.exceptions.errors import AppException
from src.models.response_model import ErrorResponse


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
        message = exc.description or exc.name or "Lỗi HTTP"
        return jsonify(_error_body(message)), exc.code or 500

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        app.logger.exception("Unhandled exception: %s", exc)
        return jsonify(_error_body(f"{exc}")), 500
