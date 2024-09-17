import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseBase

from users.error_const import constant
from users.exception import CustomException
from users.models import User


# class CustomAPIView(APIView):
#     """
#     Custom base API view that centralizes finalize_response logic.
#     """
#
#     def finalize_response(self, request, response, *args, **kwargs):
#         if isinstance(response, str):
#             # Automatically convert string responses into a standardized JSON format
#             lang = request.headers.get('lang', 'uz')
#             error_message = constant.get(response).get("message").get(lang)
#             code = constant.get(response).get("code")
#             formatted_response = {
#                 "success": False,
#                 "data": None,
#                 "error": {
#                     "message": error_message,
#                     "code": code
#                 }
#             }
#             response = Response(formatted_response, status=200)
#
#         elif isinstance(response, Response):
#             if 200 <= response.status_code < 300:
#                 # Success Response
#                 formatted_response = {
#                     "success": True,
#                     "data": json.loads(response.content.decode()),
#                     "error": None
#                 }
#             else:
#                 # Error Response
#                 formatted_response = {
#                     "success": False,
#                     "data": None,
#                     "error": {
#                         "message": response.reason_phrase,
#                         "code": response.status_code
#                     },
#                     "meta": json.loads(response.content.decode())
#                 }
#             response = Response(formatted_response, status=200)
#
#         return super().finalize_response(request, response, *args, **kwargs)
#
#
# class TestErrorAPIView(CustomAPIView):
#
#     def get(self, request, *args, **kwargs):
#         user = User.objects.filter(phone_number='998914611305').first()
#         if user is None:
#             return 'user_not_found'
#         return Response({"user_id": user.id})


class TestErrorAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(phone_number='998914611305').first()
        if user is None:
            raise CustomException('user_not_found')
        return Response({"user_id": user.id})
