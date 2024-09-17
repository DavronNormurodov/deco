from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from product.models import Category
from product.serializers.category import CategorySerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.order_by('-id')
    permission_classes = [AllowAny, ]
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        return [IsAuthenticated(), ]
