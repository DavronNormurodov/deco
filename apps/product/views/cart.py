import uuid

from django.db.models import F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Cart
from product.serializers.cart import CartSerializer, CartListSerializer
from users.services.extra_func import get_user_by_request, RESTException


class CartAddView(APIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @swagger_auto_schema(request_body=CartSerializer, manual_parameters=[
        openapi.Parameter(
            'cart_increase',
            openapi.IN_QUERY,
            description="",
            type=openapi.TYPE_BOOLEAN,
            required=False)])
    def post(self, request, *args, **kwargs):
        data = request.data
        query_params = request.query_params
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        product = validated_data.get('product')
        quantity = validated_data.get('quantity', 1)
        cart_increase = query_params.get('cart_increase')

        self.check_quantity(quantity, product)

        visitor_id, user_id = get_user_by_request(request)
        response = Response(data={
            "message": "Added cart!"
        })

        if user_id:
            return Response()

        if not visitor_id:
            visitor_id = str(uuid.uuid4())
            response.set_cookie(key="visitor_id", value=visitor_id, httponly=True, samesite=None, secure=True)

        cart, is_create = Cart.objects.update_or_create(
            visitor_id=visitor_id, product=product
        )
        if cart_increase == 'true':
            self.check_quantity(quantity + cart.quantity, product)
            cart.quantity = cart.quantity + quantity if not is_create else quantity
            cart.save()
        else:
            cart.quantity = quantity
            cart.save()

        return response

    def check_quantity(self, quantity, product):
        if quantity > product.quantity:
            raise RESTException(message="The amount is more than the number of products left!")


class CartListView(APIView):
    queryset = Cart.objects.order_by('-id')

    def get_queryset(self):
        visitor_id, user_id = get_user_by_request(self.request)
        return self.queryset.filter(visitor_id=visitor_id) if visitor_id else self.queryset.none()

    def get(self, request, *args, **kwargs):
        serializer = CartListSerializer(self.get_queryset(), many=True, context={"request": request})
        return Response(serializer.data)


class CartDeleteView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'cart_id',
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_INTEGER,
                required=True)]
    )
    def delete(self, request):
        query_params = request.query_params
        filter_kwargs = {}
        if cart_id := query_params.get('cart_id'):
            filter_kwargs['id'] = cart_id
        visitor_id, user_id = get_user_by_request(request)
        Cart.objects.filter(visitor_id=visitor_id, **filter_kwargs).delete()
        return Response(status=204)


class CartCountView(APIView):

    def get(self, request):
        visitor_id, user_id = get_user_by_request(request)
        cart = Cart.objects.filter(visitor_id=visitor_id)
        return Response({
            "count": cart.count()
        })
