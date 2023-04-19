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

    def get_subscriptions(self):
        return [user.author for user in self.subscriptions.all()]

    def get_favorites(self):
        return [favorite.recipe for favorite in self.favorites.all()]

    class Meta:
        ordering = ["username"]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписки",
        related_name="subscriptions",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчики",
        related_name="subscribers",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique subscriptions"
            )
        ]
