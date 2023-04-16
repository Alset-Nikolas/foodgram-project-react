from django.db import models

# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return str(self.name)
