class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f'HTTP {status_code}: {detail}')


class NotFound(HTTPException):
    def __init__(self, detail: str = 'Resource not found') -> None:
        super().__init__(404, detail)


class BadRequest(HTTPException):
    def __init__(self, detail: str = 'Bad Request') -> None:
        super().__init__(400, detail)


class UnProcessable(HTTPException):
    def __init__(self, detail: str = 'Unprocessable Entity') -> None:
        super().__init__(422, detail)
