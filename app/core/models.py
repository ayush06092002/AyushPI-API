"""Database Models."""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

class UserManager(BaseUserManager):
    """Manager for Users."""

    def create_user(self, email, password = None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the System."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Medicine(models.Model):
    """Medicine object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    ref_text = models.CharField(max_length=255)
    dispensing_size = models.CharField(max_length=255)
    indication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    precautions = models.TextField(max_length=255)
    preferred_use = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation of medicine."""
        return self.name

