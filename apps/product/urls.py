from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views.banner import BannerDecoView
from product.views.cart import CartAddView, CartListView, CartDeleteView, CartCountView
from product.views.category import CategoryView
from product.views.order import OrderView
from product.views.products import ProductView, ProductRateView

router = DefaultRouter()
router.register('product', ProductView, 'ProductView')
router.register('category', CategoryView, 'CategoryView')
router.register('order', OrderView, 'OrderView')

urlpatterns = [
    path('', include(router.urls)),
    path('rate', ProductRateView.as_view(), name='ProductRateView'),
    path('banner_deco/', BannerDecoView.as_view(), name='BannerDecoView'),
    path('cart/add', CartAddView.as_view(), name='CartAddView'),
    path('cart/list', CartListView.as_view(), name='CartListView'),
    path('cart/delete', CartDeleteView.as_view(), name='CartDeleteView'),
    path('cart/count', CartCountView.as_view(), name='CartCountView'),
]
