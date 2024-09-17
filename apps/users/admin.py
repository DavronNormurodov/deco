from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.utils.translation import gettext_lazy as _

from users import models
from users.models import WebSiteVisitor
from users.models.role import Role


# Register your models here.


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ('permissions',)


@admin.register(WebSiteVisitor)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("username", "visitor_id", 'user_agent')
    list_display_links = ["visitor_id", "username"]
    date_hierarchy = 'created_at'
    list_filter = (
        ('created_at', DateFieldListFilter),
    )


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_display_links = ['username']
    fieldsets = (
        (None,
         {'fields': (
             'username', 'password', 'first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'),
         {'fields': (
             'is_active', 'is_staff', 'is_superuser', 'role', 'user_permissions',)}),
        (_('Important dates'),
         {'fields': (
             'last_login',)}),
    )
    filter_horizontal = ('role', 'user_permissions',)
