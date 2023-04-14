from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


# Create your models here.
class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор",
    )
    image = models.ImageField(upload_to="recipes/")
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField()
