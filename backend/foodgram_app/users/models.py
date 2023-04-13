from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        "Email",
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        help_text="Адрес электронной почты",
    )
    username = models.CharField(
        blank=False,
        null=False,
        max_length=150,
        unique=True,
        help_text="Уникальный юзернейм",
    )
    first_name = models.CharField(
        blank=False,
        null=False,
        max_length=150,
        help_text="Имя",
    )
    last_name = models.CharField(
        blank=False,
        null=False,
        max_length=150,
        help_text="Фамилия",
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
