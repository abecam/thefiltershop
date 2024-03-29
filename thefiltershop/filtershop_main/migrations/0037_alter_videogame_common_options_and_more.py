# Generated by Django 4.2.1 on 2023-10-05 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0036_alter_entry_on_applestore_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videogame_common',
            options={'verbose_name': 'A Video Game', 'verbose_name_plural': 'Video Games'},
        ),
        migrations.AlterModelOptions(
            name='videogame_rating',
            options={'verbose_name': 'Rating with filters for one platform', 'verbose_name_plural': 'Ratings with filters by platforms'},
        ),
        migrations.AlterField(
            model_name='videogame_rating',
            name='use_psycho_tech',
            field=models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(-1)]),
        ),
    ]
