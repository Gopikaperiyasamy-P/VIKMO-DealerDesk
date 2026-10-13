from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.exceptions import (
    ValidationError,
    APIException,
    NotFound,
    NotAuthenticated,
    PermissionDenied,
    MethodNotAllowed,
)


class CustomAPIException(APIException):
    def __init__(self, code="VALIDATION_ERROR", message="An error occurred", details=None, status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or []
        self.status_code = status_code


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        return Response(
            {
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
            status=exc.status_code,
        )

    if isinstance(exc, Http404) or isinstance(exc, NotFound):
        return Response(
            {
                "error": {
                    "code": "NOT_FOUND",
                    "message": "Resource not found",
                    "details": [str(exc)] if str(exc) else [],
                }
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, ValidationError):
        details = []
        if isinstance(exc.detail, dict):
            for k, v in exc.detail.items():
                if isinstance(v, list):
                    for item in v:
                        details.append(f"{k}: {item}")
                else:
                    details.append(f"{k}: {v}")
        elif isinstance(exc.detail, list):
            for item in exc.detail:
                details.append(str(item))
        else:
            details.append(str(exc.detail))
        return Response(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation error: " + (details[0] if details else "Invalid input"),
                    "details": details,
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if response is not None:
        code = "ERROR"
        if response.status_code == 404:
            code = "NOT_FOUND"
        elif response.status_code == 400:
            code = "VALIDATION_ERROR"
        elif response.status_code == 409:
            code = "CONFLICT"

        details = []
        if isinstance(response.data, dict) and "error" in response.data:
            return response
        if isinstance(response.data, dict):
            for k, v in response.data.items():
                details.append(f"{k}: {v}")
        elif isinstance(response.data, list):
            details = [str(x) for x in response.data]
        else:
            details = [str(response.data)]

        return Response(
            {
                "error": {
                    "code": code,
                    "message": details[0] if details else "An error occurred",
                    "details": details,
                }
            },
            status=response.status_code,
        )

    return Response(
        {
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc),
                "details": [],
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
