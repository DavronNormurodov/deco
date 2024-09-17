import django_filters
from django_filters import FilterSet

from users.models import User


class UserFilter(FilterSet):
    role = django_filters.NumberFilter(field_name='role', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
