from django.db import models
from django.db.models import SET_NULL, CASCADE

from common.models import BaseModel


class Cart(BaseModel):
    user = models.ForeignKey('users.User', on_delete=SET_NULL, blank=True, null=True)
    visitor_id = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey('product.Product', on_delete=CASCADE, related_name='carts')
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'carts'
