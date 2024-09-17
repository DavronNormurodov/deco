import threading

from django.db import models

from common.models import BaseModel
from common.services.redis import write_to_redis


class WebSiteVisitor(BaseModel):
    user_agent = models.TextField(null=True, blank=True)
    visitor_id = models.CharField(max_length=300)
    username = models.CharField(max_length=255, null=True, blank=True)

    def __int__(self):
        return self.id

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        from datetime import datetime

        current_date = datetime.now().strftime("%Y-%m-%d")
        threading.Thread(target=write_to_redis, args=[self.visitor_id, current_date, 86400]).start()
        return super(WebSiteVisitor, self).save()

    class Meta:
        db_table = 'web_site_visitors'
