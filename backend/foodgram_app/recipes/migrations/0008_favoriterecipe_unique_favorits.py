# Generated by Django 4.2 on 2023-04-19 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_favoriterecipe'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique favorits'),
        ),
    ]
