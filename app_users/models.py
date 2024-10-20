from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserModelManager


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to='profile-images/', default='profile-images/user-default.png', blank=True)
    objects = UserModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def fullname(self):
        return self.get_full_name()

    def __str__(self):
        return self.username
