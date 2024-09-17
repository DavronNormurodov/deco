from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from core.settings import CURRENT_HOST
from users.models import User


class RegistrationUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, min_length=4)
    first_name = serializers.CharField(max_length=255, )
    last_name = serializers.CharField(max_length=255, required=False)
    phone_number = serializers.CharField(max_length=14, error_messages={
        "unique": _("A user with that phone number already exists.")}, required=False)
    roles = serializers.ListField(child=serializers.IntegerField())
    profile_picture = serializers.ImageField(required=False)
    email = serializers.EmailField(required=False)


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'permissions', 'profile_picture',
            'is_superuser',
            'is_active',
            'full_name'
        )

    #
    # def to_representation(self, instance):
    #     repr_r = super().to_representation(instance)
    #     repr_r['roles'] = instance.role.values('id', 'name', 'unique_name')
    #
    #     return repr_r

    def get_permissions(self, obj):
        roles = obj.role.all()
        unique_names = [role.unique_name for role in roles]
        return unique_names

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserUpdateSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(child=serializers.IntegerField(), required=False)
    email = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    username = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'phone_number', 'email', 'roles', 'is_active']
        extra_kwargs = {
            "password": {"required": False},
            "username": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "phone_number": {"required": False},
            # "email": {"required": False},
            "is_active": {"required": False, "default": True}
        }


class UserTokenSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "Неверный пароль или имя пользователя!"
    }

    def get_token(self, user):
        token = super().get_token(user)
        user_data = UserSerializer(
            user,
            context={'request': self.context['request']}
        ).data
        token['user_data'] = user_data
        return token
