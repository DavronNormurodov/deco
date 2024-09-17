
import json
import traceback
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from users.error_const import constant
from users.exception import CustomException

class StandardResponseMiddleware(MiddlewareMixin):
    """
    Middleware to standardize the response format.
    """

    def process_response(self, request, response):
        # Skip formatting for already formatted responses
        if isinstance(response, JsonResponse):
            return response

        if 200 <= response.status_code < 300:
            # Success Response
            formatted_response = {
                "success": True,
                "data": json.loads(response.content.decode()),
                "error": None
            }
        else:
            # Error Response
            formatted_response = {
                "success": False,
                "data": None,
                "error": {
                    "message": response.reason_phrase,
                    "code": response.status_code
                },
                "meta": json.loads(response.content.decode())
            }

        return JsonResponse(formatted_response, status=200)

    def process_exception(self, request, exception):
        lang = request.headers.get('lang', 'uz')
        # Log exception for debugging purposes
        # print(traceback.format_exc())

        # Customize the error response here based on exception types
        if isinstance(exception, CustomException):
            key = exception.args[0]
            error_message = constant.get(key).get("message").get(lang)
            code = constant.get(key).get("code")
        else:
            error_message = str(exception)
            code = 2000

        formatted_response = {
            "success": False,
            "data": None,
            "error": {
                "message": error_message,
                "code": code
            }
        }

        return JsonResponse(formatted_response, status=200)


class GlobalExceptionHandlerMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        # Log exception for debugging purposes
        # print(traceback.format_exc())

        error_message = str(exception)
        code = 2000

        formatted_response = {
            "success": False,
            "data": None,
            "error": {
                "message": error_message,
                "code": code
            }
        }

        # return JsonResponse(formatted_response, status=200)
        return Response(formatted_response, status=200)
