from django.contrib.auth.models import Permission
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.pagination import PaginationView, MyPagination
from users.models import Role
from users.serializers.role_permission import RoleCreateSerializer, RoleSerializer
from users.services.extra_func import RESTException
from users.views.db_service import get_all_roles, get_role_by_id, update_or_delete_role_by_id


class RoleView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        roles = get_all_roles()
        return Response(data=roles)

    @swagger_auto_schema(request_body=RoleCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RoleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        permissions = validated_data.pop('permissions', False)

        try:
            role = Role.objects.create(**validated_data)
            if permissions:
                role.permissions.set(permissions)
            # role = Role.objects.bulk_create(name=validated_data['name'])
        except Exception as error:
            raise APIException(detail=str(error))
        return Response(data=validated_data)


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        role = get_role_by_id(pk=kwargs['pk'])
        serializer = RoleSerializer(role)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=RoleSerializer)
    def patch(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        permissions = False
        if 'permissions' in validated_data:
            permissions = validated_data.pop('permissions')

        try:
            role = update_or_delete_role_by_id(role_id=kwargs['pk'])
            if permissions:
                role[0].permissions.set(permissions)
            role.update(**validated_data)
        except Exception as error:
            raise RESTException(detail={
                "success": False,
                "error": str(error)})

        return Response(data="Successfully updated!", status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        role = get_role_by_id(kwargs['pk'])
        role.delete()
        return Response(data="Deleted!", status=status.HTTP_204_NO_CONTENT)


class PermissionView(APIView, PaginationView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = MyPagination

    def get(self, reuqest, *args, **kwargs):
        permissions = Permission.objects.values('id', 'name', 'content_type_id')
        page = self.paginate_queryset(permissions)

        return self.get_paginated_response(page)
