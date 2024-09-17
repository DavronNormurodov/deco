from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Model, DateTimeField, BooleanField

from common.queryset import DeleteManager


def default_json():
    return {"ru": "", "uz": "", "en": ""}


class BaseModel(Model):
    modified_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AttachmentModel(Model):
    attachments = GenericRelation('utils.Attachment')

    class Meta:
        abstract = True


class DeleteModel(Model):
    is_delete = BooleanField(default=False)

    objects = DeleteManager()

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.is_delete = True
        self.save()
