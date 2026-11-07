from .base_exception import BaseFastapiAppException


class BadRequestError(BaseFastapiAppException):
    def __init__(self, code="CORE-REQ-400", message="Bad Request", http_status_code=400, **kwargs):
        super().__init__(code, message, http_status_code=http_status_code, **kwargs)


class UnauthorizedError(BaseFastapiAppException):
    def __init__(self, code="CORE-AUT-401", message="Unauthorized", http_status_code=401, **kwargs):
        super().__init__(code, message, http_status_code=http_status_code, **kwargs)


class ForbiddenError(BaseFastapiAppException):
    def __init__(self, code="CORE-AUT-403", message="Forbidden", http_status_code=403, **kwargs):
        super().__init__(code, message, http_status_code=http_status_code, **kwargs)


class NotFoundError(BaseFastapiAppException):
    def __init__(self, code="CORE-REQ-404", message="Not Found", http_status_code=404, **kwargs):
        super().__init__(code, message, http_status_code=http_status_code, **kwargs)


class MethodNotAllowedError(BaseFastapiAppException):
    def __init__(
        self,
        code="CORE-REQ-405",
        message="Method Not Allowed",
        http_status_code=405,
        **kwargs,
    ):
        super().__init__(code, message, http_status_code=http_status_code, **kwargs)


class InternalServerError(BaseFastapiAppException):
    def __init__(
        self,
        code="CORE-REQ-500",
        message="Internal Server Error",
        http_status_code=500,
        **kwargs,
    ):
        super().__init__(code, message, http_status_code=http_status_code, **kwargs)
