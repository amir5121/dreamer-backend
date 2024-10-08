import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField

from utils import constants


class DreamerUserManager(UserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.pop("username", None)
        return super(DreamerUserManager, self).create_user(email, email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    avatar = VersatileImageField(upload_to='avatars/', blank=True, null=True)
    last_app_open = models.DateTimeField(_('last login'), blank=True, null=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    gender = models.CharField(max_length=8, choices=constants.GENDERS, blank=True, null=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = DreamerUserManager()

    def save(self, *args, **kwargs):
        self.last_name = self.first_name + " " + self.last_name
        self.first_name = ""
        return super(User, self).save(*args, **kwargs)

    @property
    def get_full_name(self):
        full_name = super(User, self).get_full_name()
        if full_name:
            return full_name
        return "Dreamer"
