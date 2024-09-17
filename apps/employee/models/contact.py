from django.db import models

from common.models import BaseModel, default_json


class Contact(BaseModel):
    class ContactType(models.TextChoices):
        PLACE = 'PLACE'
        SOCIAL = 'SOCIAL'
        ABOUT_US = 'ABOUT_US'

    title = models.JSONField(default=default_json, blank=True, null=True)
    description = models.JSONField(default=default_json, blank=True, null=True)  # about_us
    address = models.CharField(max_length=255, blank=True, null=True)  # place
    phone_number = models.CharField(max_length=13, blank=True, null=True)  # place
    contact_type = models.CharField(max_length=15, choices=ContactType.choices, default=ContactType.PLACE)
    social_link = models.CharField(max_length=155, blank=True, null=True)  # social
    file = models.ImageField(upload_to='contact/', blank=True, null=True)  # about_us  # social
    location = models.JSONField(blank=True, null=True)  # place

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'contacts'


class Social(BaseModel):
    instagram = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)

    def __int__(self):
        return self.id
