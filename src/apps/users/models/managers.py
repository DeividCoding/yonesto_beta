from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager, models.Manager):
    def _create_user(
        self,
        user_name,
        email,
        password,
        is_staff,
        is_superuser,
        is_active,
        **extra_fields
    ):
        user = self.model(
            user_name=user_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
        self,
        user_name,
        email,
        password=None,
        is_staff=False,
        is_active=False,
        **extra_fields
    ):
        return self._create_user(
            user_name, email, password, is_staff, False, is_active, **extra_fields
        )

    def create_superuser(
        self,
        user_name,
        email,
        password=None,
        is_staff=True,
        is_active=True,
        **extra_fields
    ):
        return self._create_user(
            user_name, email, password, is_staff, True, is_active, **extra_fields
        )
