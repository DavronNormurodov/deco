import threading
import uuid

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from product.models.banner import BannerDeco
from product.serializers.banner import BannerDecoSerializer
from users.services.visitors import calculate_site_visitors, visitor_web_site


class BannerDecoView(ListAPIView):
    queryset = BannerDeco.objects.filter(is_active=True)
    serializer_class = BannerDecoSerializer
    permission_classes = [AllowAny, ]
    swagger_tag = ['product']
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)

        response_result = visitor_web_site(request, response)

        return response_result
