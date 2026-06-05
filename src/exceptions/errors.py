class AppException(Exception):
    """Exception gốc của ứng dụng."""

    status_code: int = 500

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(message)


class BadRequestError(AppException):
    status_code = 400


class NotFoundError(AppException):
    status_code = 404

    def __init__(self, message: str = "Không tìm thấy."):
        super().__init__(message)


class ServiceUnavailableError(AppException):
    status_code = 503

    def __init__(self, message: str = "Dịch vụ tạm thời không khả dụng."):
        super().__init__(message)


class InternalServerError(AppException):
    status_code = 500

    def __init__(self, message: str = "Lỗi hệ thống. Vui lòng thử lại sau."):
        super().__init__(message)
