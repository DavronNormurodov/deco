from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.pagination import PaginationView, MyPagination
from users.filter import UserFilter
from users.models import User
from users.serializers.user import UserSerializer, UserUpdateSerializer
from users.services.extra_func import RESTException
from users.views.db_service import get_user_by_id, update_or_delete_user_by_id


class UserView(views.APIView, PaginationView):
    queryset = User.objects.filter(is_delete=False).order_by('id')
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserFilter
    search_fields = ['first_name', 'last_name', 'username']

    def get(self, request, *args, **kwargs):
        users = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(users)
        serializer = UserSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class UserDetail(views.APIView):
    # parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):

        """ Get currently user """
        user_id = kwargs['user_id']

        user_in_db = get_user_by_id(user_id=user_id)
        serializer = UserSerializer(user_in_db, context={"request": request})

        return Response(data=serializer.data, status=200)

    @swagger_auto_schema(request_body=UserUpdateSerializer,
                         operation_description="You should give user image with 'profile_picture' variable")
    def patch(self, request, *args, **kwargs):

        """ Get currently user """
        user_id = kwargs['user_id']

        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        profile_picture = request.FILES.get('profile_picture', False)

        password = False
        if 'password' in validated_data:
            password = validated_data.pop('password')

        try:
            users = update_or_delete_user_by_id(user_id)

            """ Attach roles for users """
            if 'roles' in validated_data:
                roles = validated_data.pop('roles')
                for user in users:
                    user.role.set(roles)

            users.update(**validated_data)

            """ Change password """
            if password:
                user_p = get_user_by_id(user_id)
                user_p.set_password(raw_password=password)
                user_p.save()

            users[0].save()
        except Exception as error:
            raise RESTException(detail=error)

        if profile_picture or request.data.get('profile_picture'):
            user = get_user_by_id(user_id=user_id)
            if request.data.get('profile_picture'):
                user.profile_picture = profile_picture
                user.save()
            else:
                user.profile_picture = profile_picture
                user.save()
                validated_data['profile_picture'] = user.profile_picture.name

        return Response(data=validated_data, status=200)

    def delete(self, request, *args, **kwargs):

        """ Get currently user """
        user_id = kwargs['user_id']

        user = get_user_by_id(user_id)
        user.is_delete = True
        user.save()

        return Response(data="User was deleted")
