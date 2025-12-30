from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.utils import get_upload_path

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to=get_upload_path,
        null=True,
        blank=True,
        verbose_name="Avatar"
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Bio")
    
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
