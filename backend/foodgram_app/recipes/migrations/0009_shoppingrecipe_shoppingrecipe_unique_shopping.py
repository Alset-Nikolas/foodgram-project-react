# Generated by Django 4.2 on 2023-04-20 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_favoriterecipe_unique_favorits'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Покупки',
                'verbose_name_plural': 'Покупка',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingrecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique shopping'),
        ),
    ]