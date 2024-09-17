from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

import os
# from shared.django.model import BaseModel, DeleteModel
from common.models import BaseModel, DeleteModel
from users.services.managers import UserManager
from users.models.permission import CustomPermissionsMixin


def user_picture_path(instance, filename):
    # Get Current Date

    extension = "." + filename.split('.')[-1]

    # Filename reformat
    filename_reformat = str(instance.username) + extension

    return os.path.join("users/", filename_reformat)


phone_regex = RegexValidator(
    regex=r'^+998[0-9]{9}$',
    message="Phone number must be entered in the format: '+998 [XX] [XXX XX XX]'. Up to 12 digits allowed."
)


class User(AbstractBaseUser, CustomPermissionsMixin, BaseModel, DeleteModel):
    """ User Table """

    username = models.CharField(max_length=30, unique=True, verbose_name='username', help_text=_(
        "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
    ),
                                error_messages={
                                    "unique": _("A user with that username already exists."),
                                }, )

    first_name = models.CharField(max_length=255, verbose_name='first name')
    last_name = models.CharField(max_length=255, verbose_name='last name', blank=True, null=True)

    email = models.EmailField(max_length=100, verbose_name='email', error_messages={
        "unique": _("A user with that email already exists.")
    }, blank=True, null=True)
    phone_number = models.CharField(max_length=20, error_messages={
        "unique": _("A user with that phone number already exists.")}, blank=True, null=True)

    """ Profile picture Upload """
    profile_picture = models.ImageField(upload_to=user_picture_path, blank=True,
                                        null=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    """ Authorization field """
    USERNAME_FIELD = 'username'

    """ User Manager """
    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.last_name, self.first_name)
        return full_name.strip()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'

