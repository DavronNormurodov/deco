import os
from django.db import models
from django.db.models import SET_NULL, CASCADE

from common.models import BaseModel


def get_upload_path(instance, filename):
    return os.path.join(f'{instance.product._meta.db_table}', f'{instance.product.id}', filename)


class Product(BaseModel):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    price = models.FloatField()
    sale_price = models.FloatField(blank=True, null=True)
    exchange_rate = models.CharField(max_length=100, blank=True, null=True)
    sale_exchange_rate = models.CharField(max_length=100, blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    is_banner = models.BooleanField(default=False)
    can_estimate = models.BooleanField(default=True)
    banner_photo = models.ImageField(upload_to='banner/', blank=True, null=True)

    rate = models.FloatField(default=0)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    category = models.ForeignKey('product.Category', SET_NULL, blank=True, null=True, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'


class ProductRate(BaseModel):
    product = models.ForeignKey('product.Product', CASCADE, related_name='product_rates')
    rate = models.FloatField()
    author = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'product_rates'


class ProductImage(BaseModel):
    product = models.ForeignKey('product.Product', CASCADE, related_name='product_images')
    photo = models.ImageField(upload_to=get_upload_path)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'product_images'