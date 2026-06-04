class ApiError(Exception):
    pass


class ApiTimeoutError(ApiError):
    pass


class ApiConnectionError(ApiError):
    pass