# Generated by Django 4.2 on 2023-04-15 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_alter_tags_options'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipes.RecipeTags', to='tags.tags', verbose_name='Теги'),
        ),
    ]