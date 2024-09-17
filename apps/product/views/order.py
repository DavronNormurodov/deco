from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from product.models.order import Order
from product.serializers.order import OrderSerializer


class OrderView(ModelViewSet):
    queryset = Order.objects.order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post']
