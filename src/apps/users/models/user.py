from common.abstract_models import BaseModelClass
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from model_utils.models import TimeStampedModel
from users.models.managers import UserManager


def user_directory_path(instance, filename):

    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.id, filename)


class User(AbstractBaseUser, PermissionsMixin, BaseModelClass):
    class Meta:
        db_table = "User"
        verbose_name = "User"
        verbose_name_plural = "Users"

    CHOICES_GENDER = (("M", "Male"), ("F", "Feminine"), ("O", "Others"))

    objects = UserManager()

    user_name = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)
    photo = models.ImageField(
        upload_to=user_directory_path,
        null=True,
    )
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER, blank=True)

    # 'staff' is the permission that users have that can access the django admin
    is_staff = models.BooleanField(default=False)

    # 'active' means if a user is already ready to work
    is_active = models.BooleanField(default=False)

    # Specifying which field will be used in the django admin login
    USERNAME_FIELD = "user_name"

    # Specifying the fields that will be requested in the console when creating a user
    REQUIRED_FIELDS = ["email"]
