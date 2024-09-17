from django.db import models

from common.models import BaseModel


class Category(BaseModel):
    name = models.JSONField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'categories'