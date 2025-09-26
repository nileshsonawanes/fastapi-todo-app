from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from fastapi import status
from fastapi.encoders import jsonable_encoder

T = TypeVar('T', bound=BaseModel)

class ResponseModel(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None

    class Config:
        json_encoders = {
            # Add any custom encoders here
        }

def create_response(
    data: Any = None,
    message: str = "Operation completed successfully",
    status_code: int = status.HTTP_200_OK,
    success: bool = True
) -> Dict[str, Any]:
    """
    Create a standardized API response.
    
    Args:
        data: The data to include in the response
        message: A message describing the result
        status_code: HTTP status code
        success: Whether the operation was successful
        
    Returns:
        A dictionary with the response data
    """
    response_data = {
        "success": success,
        "message": message,
    }
    
    if data is not None:
        response_data["data"] = jsonable_encoder(data, by_alias=False)
    
    return response_data

def error_response(
    message: str = "An error occurred",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    errors: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        errors: Additional error details
        
    Returns:
        A dictionary with the error response
    """
    response = {
        "success": False,
        "message": message,
    }
    
    if errors:
        response["errors"] = errors
    
    return response
