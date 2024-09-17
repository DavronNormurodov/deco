from rest_framework.serializers import ModelSerializer

from product.models import Cart
from product.serializers.products import ProductShortListSerializer


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']


class CartListSerializer(ModelSerializer):
    product = ProductShortListSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']
