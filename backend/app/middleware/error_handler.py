"""
Error handling middleware for Multi-Agent AI Chat System.

This middleware provides centralized error handling and user-friendly error responses.
"""
import logging
from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware for centralized error handling.
    
    Catches exceptions and converts them to appropriate HTTP responses
    with user-friendly error messages while logging detailed error information.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with error handling.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/endpoint in the chain
            
        Returns:
            HTTP response or error response
        """
        try:
            # Process request normally
            response = await call_next(request)
            return response
            
        except HTTPException:
            # FastAPI HTTP exceptions - let them pass through
            raise
            
        except SQLAlchemyError as e:
            # Database errors
            logger.error(
                f"Database error in {request.method} {request.url.path}",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "request_id": getattr(request.state, "request_id", "unknown")
                },
                exc_info=True
            )
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Database Error",
                    "message": "A database error occurred. Please try again later.",
                    "type": "database_error"
                }
            )
            
        except ValueError as e:
            # Validation errors
            logger.warning(
                f"Validation error in {request.method} {request.url.path}",
                extra={
                    "error": str(e),
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
            
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Validation Error",
                    "message": str(e),
                    "type": "validation_error"
                }
            )
            
        except KeyError as e:
            # Missing data errors
            logger.warning(
                f"Key error in {request.method} {request.url.path}",
                extra={
                    "error": str(e),
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
            
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Missing Data",
                    "message": f"Required data is missing: {str(e)}",
                    "type": "missing_data_error"
                }
            )
            
        except PermissionError as e:
            # Permission/authorization errors
            logger.warning(
                f"Permission error in {request.method} {request.url.path}",
                extra={
                    "error": str(e),
                    "request_id": getattr(request.state, "request_id", "unknown")
                }
            )
            
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Permission Denied",
                    "message": "You don't have permission to perform this action.",
                    "type": "permission_error"
                }
            )
            
        except Exception as e:
            # Unexpected errors
            logger.error(
                f"Unexpected error in {request.method} {request.url.path}",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "request_id": getattr(request.state, "request_id", "unknown")
                },
                exc_info=True
            )
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred. Please try again later.",
                    "type": "internal_server_error"
                }
            )
