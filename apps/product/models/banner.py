from django.db import models

from common.models import BaseModel


class BannerDeco(BaseModel):
    photo = models.ImageField(upload_to='banner/')
    is_active = models.BooleanField(default=True)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'banner_deco'
