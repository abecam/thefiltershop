# Generated by Django 4.2.1 on 2023-09-06 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0013_alter_entity_crapometer_alter_entity_general_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='online_shop',
            name='they_have_made_it',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='physical_shop',
            name='they_have_made_it',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='software',
            name='they_have_made_it',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='videogame_common',
            name='they_have_made_it',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)]),
        ),
    ]
