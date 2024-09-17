from django.db import models
from django.db.models import CASCADE, TextChoices

from common.models import BaseModel


class Order(BaseModel):
    class OrderStatus(TextChoices):
        created = 'created'
        in_progress = 'in_progress'
        finished = 'finished'

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    mail = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=OrderStatus.choices, default=OrderStatus.created)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'order'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=CASCADE, related_name='order_item')
    product = models.ForeignKey('product.Product', on_delete=CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_item'
