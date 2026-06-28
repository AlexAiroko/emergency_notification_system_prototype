from fastapi import status


class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "app_error"
    
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"


class ValidationError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "validation_error"
