from django_filters import FilterSet

from product.models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = ['category', ]