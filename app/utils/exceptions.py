from fastapi import status
from fastapi.exceptions import HTTPException
from typing import Any, Dict, Optional

class AppException(HTTPException):
    """Base exception for application-specific exceptions."""
    def __init__(
        self,
        status_code: int,
        detail: str = None,
        headers: Dict[str, Any] = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail or "An error occurred",
            headers=headers or {},
        )

class BadRequestException(AppException):
    """Raised when the request is invalid or malformed."""
    def __init__(self, detail: str = "Bad Request") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

class UnauthorizedException(AppException):
    """Raised when authentication is required and has failed or has not been provided."""
    def __init__(self, detail: str = "Not authenticated") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenException(AppException):
    """Raised when the user doesn't have enough permissions to access a resource."""
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

class NotFoundException(AppException):
    """Raised when a resource is not found."""
    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )

class ConflictException(AppException):
    """Raised when a conflict with an existing resource occurs."""
    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )

class ValidationException(AppException):
    """Raised when data validation fails."""
    def __init__(self, errors: Dict[str, Any], detail: str = "Validation error") -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )
        self.errors = errors

class InternalServerError(AppException):
    """Raised when an unexpected error occurs."""
    def __init__(self, detail: str = "Internal server error") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
