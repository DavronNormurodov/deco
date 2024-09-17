from django.urls import path, include
from rest_framework.routers import DefaultRouter

from employee.views.contact import ContactView, SocialView

router = DefaultRouter()
router.register('contact', ContactView, 'ContactView')
router.register('social', SocialView, 'SocialView')

urlpatterns = [
    path('', include(router.urls)),
]
