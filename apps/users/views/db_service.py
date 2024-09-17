import datetime
import random

from django.utils import timezone

from users.models import User, Role
from users.services.extra_func import RESTException


def get_all_users():
    try:
        users = User.objects.filter(is_delete=False).order_by('id')
    except Exception as e:
        raise RESTException(detail="Этот пользователь не существует!", status_code=404)
    return users


def get_user_by_id(user_id):
    try:
        user = User.objects.get(id=user_id, is_delete=False)
    except Exception as e:
        raise RESTException(detail="Этот пользователь не существует!", status_code=404)
    return user


def update_or_delete_user_by_id(user_id):
    try:
        user = User.objects.filter(id=user_id, is_delete=False)
    except Exception as e:
        raise RESTException(detail="Этот пользователь не существует!", status_code=404)
    return user


def get_all_roles():
    roles = Role.objects.values('id', 'name', 'unique_name', 'quantity_work')
    return roles


def get_role_by_id(pk):
    role = ''
    try:
        role = Role.objects.get(id=pk)
    except Exception as error:
        raise RESTException(detail=error)
    return role


def update_or_delete_role_by_id(role_id):
    role = Role.objects.filter(id=role_id)
    return role
