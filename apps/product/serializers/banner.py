from rest_framework.serializers import ModelSerializer

from product.models.banner import BannerDeco


class BannerDecoSerializer(ModelSerializer):
    class Meta:
        model = BannerDeco
        fields = ['photo']
