from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from employee.models import Contact, Social
from employee.serializers.contact import ContactSerializer, SocialSerializer


class ContactView(ModelViewSet):
    queryset = Contact.objects.order_by('-id')
    permission_classes = [AllowAny, ]
    serializer_class = ContactSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['contact_type']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        return [IsAuthenticated(), ]


class SocialView(ModelViewSet):
    queryset = Social.objects.order_by('-id')
    permission_classes = [AllowAny, ]
    serializer_class = SocialSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny(), ]
        return [IsAuthenticated(), ]
