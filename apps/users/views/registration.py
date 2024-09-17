from django.db import transaction
from drf_yasg import views
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from users.models import User
from users.serializers.user import UserTokenSerializer, RegistrationUserSerializer
from users.services.extra_func import RESTException


class UserRegister(views.APIView):
    """ User Registration class """
    # parser_classes = (MultiPartParser, FormParser)

    @transaction.atomic()
    @swagger_auto_schema(request_body=RegistrationUserSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RegistrationUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        roles = validated_data.pop('roles')

        password = validated_data.pop('password')

        """ Create User """
        try:
            user = User.objects.create_user(password=password, **validated_data)
            for role in roles:
                user.role.add(role)
            user.save()
        except Exception as error:
            raise RESTException(
                detail={
                    "success": False,
                    "error": str(error)
                },
                status_code=400)

        if 'profile_picture' in validated_data:
            validated_data.pop('profile_picture')

        return Response(validated_data, status=status.HTTP_201_CREATED)


class UserToken(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = UserTokenSerializer
