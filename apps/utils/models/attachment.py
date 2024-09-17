import os
from tkinter import CASCADE

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, PositiveIntegerField
from rest_framework.fields import CharField, FileField

from common.models import BaseModel


def get_upload_path(instance, filename):
    return os.path.join(f'{instance.content_type.model}', f'{instance.object_id}', filename)


class Attachment(BaseModel):
    # Relationships
    title = CharField(max_length=255, null=True, blank=True)
    content_type = ForeignKey(ContentType, CASCADE, 'attachments')
    content_object = GenericForeignKey('content_type', 'object_id')

    # Fields
    object_id = PositiveIntegerField()
    file = FileField(upload_to=get_upload_path, max_length=10000)

    def __str__(self):
        return str(self.id)
