from django.db.models import Sum, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from drf_toolmux.exception import RESTException
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from product.models import Product, ProductRate
from product.serializers.products import ProductSerializer, ProductRateSerializer, ProductListSerializer


class ProductView(ModelViewSet):
    queryset = Product.objects.prefetch_related('carts').order_by('-id')
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'is_banner', 'is_sale']
    search = ['name']
    swagger_tag = ['product']

    def list(self, request, *args, **kwargs):
        is_banner = request.query_params.get('is_banner', False)
        queryset = self.filter_queryset(self.get_queryset().filter(is_banner=is_banner))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        return [IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return self.serializer_class


class ProductRateView(APIView):
    permission_classes = [AllowAny]
    swagger_tag = ['product']

    @swagger_auto_schema(request_body=ProductRateSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ProductRateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        product = validated_data.pop('product', None)

        if product.can_estimate:
            ProductRate.objects.create(product=product, **validated_data)
            rating = Product.objects.filter(id=product.id).annotate(rate_sum=Sum('product_rates__rate'),
                                                                    rate_count=Count('product_rates__id',
                                                                                     distinct=True)).first()
            rating.rate = round(rating.rate_sum / rating.rate_count, 2)
            rating.save()

        return Response("Rated!")
