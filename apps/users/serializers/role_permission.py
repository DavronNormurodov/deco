from django.contrib.auth.models import Permission
from rest_framework import serializers

from users.models import Role


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        Model = Permission
        field = ['__all__']


class RoleCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    unique_name = serializers.ChoiceField(choices=Role.UniqueType.choices)
    permissions = serializers.ListSerializer(child=serializers.IntegerField(required=False), required=False)


class RoleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    unique_name = serializers.ChoiceField(choices=Role.UniqueType.choices)
    permissions = serializers.ListSerializer(child=serializers.IntegerField(), required=False)


class RolePermissionsDeleteSerializer(serializers.Serializer):
    permission_id = serializers.ListSerializer(child=serializers.IntegerField())