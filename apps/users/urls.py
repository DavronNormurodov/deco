from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views.registration import UserToken, UserRegister
from users.views.roles import RoleView, PermissionView, RoleDetailView
from users.views.test_exception_handling import TestErrorAPIView
from users.views.user_detail import UserDetail, UserView

urlpatterns = [
    # Jwt Token
    path('login', UserToken.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/register', UserRegister.as_view(), name='user-register'),
    path('users', UserView.as_view(), name='user'),
    path('users/<int:user_id>', UserDetail.as_view(), name='user-get-update-delete'),

    path('users/error-handling-test', TestErrorAPIView.as_view(), name='test'),

    path('roles', RoleView.as_view(), name='get-roles'),
    path('roles/<int:pk>', RoleDetailView.as_view(), name='get-detail-roles'),

    # permissions
    path('permissions', PermissionView.as_view(), name='get-permission'),

]
