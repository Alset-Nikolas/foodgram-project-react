# Generated by Django 4.2 on 2023-04-26 08:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_favoriterecipe_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_shopping', to='recipes.recipe', verbose_name='рецепт'),
        ),
    ]
