import logging
import traceback
import sys
from rest_framework.views import exception_handler
from rest_framework import status
from django.http import Http404
from rest_framework.exceptions import (
    ValidationError,
    PermissionDenied,
    AuthenticationFailed,
)
from .success_wrapper import error_response

logger = logging.getLogger("api_errors")


def custom_exception_handler(exc, context):
    """
    Global exception handler for DRF
    """

    exc_type, exc_value, exc_tb = sys.exc_info()

    formatted_tb = traceback.format_exception(exc_type, exc_value, exc_tb)

    tb_last = traceback.extract_tb(exc_tb)[-1]

    file_name = tb_last.filename
    line_no = tb_last.lineno
    func_name = tb_last.name
    code_line = tb_last.line
    
    extra_t={
            "view": context.get("view").__class__.__name__ if context.get("view") else None,
            "exception_type": exc_type.__name__,
            "exception_message": str(exc),
            "file": file_name,
            "line": line_no,
            "function": func_name,
            "code": code_line,
            "traceback": "".join(formatted_tb),
        },

    logger.error(
        "Unhandled exception occurred",
        # extra = str(exc),
        exc_info=True, 
    )

    response = exception_handler(exc, context)

    # Validation errors (400)
    if isinstance(exc, ValidationError):
        return error_response(
            message="Validation failed",
            errors=exc.detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Authentication errors (401)
    if isinstance(exc, AuthenticationFailed):
        return error_response(
            message="Authentication failed",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Permission errors (403)
    if isinstance(exc, PermissionDenied):
        return error_response(
            message="Permission denied",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # Not found (404)
    if isinstance(exc, Http404):
        return error_response(
            message="Resource not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if response is not None:
        return error_response(
            message="Request failed",
            errors=response.data,
            status_code=response.status_code,
        )

    # Fallback (500)
    return error_response(
        message="Internal server error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
