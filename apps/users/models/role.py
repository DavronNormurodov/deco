from django.contrib.auth.models import Group, Permission, GroupManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    class UniqueType(models.TextChoices):
        ADMIN = 'admin'
        EMPLOYEE = 'employee'

    name = models.CharField(_("name"), max_length=150, unique=True)
    unique_name = models.CharField(max_length=15, choices=UniqueType.choices, default=UniqueType.EMPLOYEE)

    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")
        db_table = 'roles'

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)
