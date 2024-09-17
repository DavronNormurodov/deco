from rest_framework import serializers

from product.models import Product, ProductImage, ProductRate
from product.serializers.category import CategorySerializer
from product.services import delete_files
from users.services.extra_func import get_user_by_request


class ProductImages(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'photo']


class ProductListSerializer(serializers.ModelSerializer):
    product_images = ProductImages(many=True, read_only=True)
    category = CategorySerializer(required=False)
    cart_count = serializers.SerializerMethodField()

    # category = serializers.JSONField(source='category.name', required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def get_cart_count(self, obj):
        visitor_id, user_id = get_user_by_request(self.context.get('request'))
        count = obj.carts.filter(visitor_id=visitor_id).first() if visitor_id else None
        if count:
            return count.quantity
        return 0


class ProductShortListSerializer(serializers.ModelSerializer):
    product_images = ProductImages(many=True, read_only=True)

    # category = serializers.JSONField(source='category.name', required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'sale_price', 'exchange_rate', 'quantity', 'product_images']


class ProductSerializer(serializers.ModelSerializer):
    # product_images = ProductImages(many=True, read_only=True)
    can_estimate = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product = super(ProductSerializer, self).create(validated_data)
        images = self.context.get('request').FILES.getlist('images', [])

        for image in images:
            ProductImage.objects.create(product_id=product.id, photo=image)
        return product

    def update(self, instance, validated_data):
        images = self.context.get('request').FILES.getlist('images', [])

        if images:
            old_images = ProductImage.objects.filter(product_id=instance.id)
            delete_files(query=old_images)

        for image in images:
            ProductImage.objects.create(product_id=instance.id, photo=image)

        return super(ProductSerializer, self).update(instance, validated_data)


class ProductRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRate
        fields = '__all__'
