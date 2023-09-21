# Generated by Django 4.2.1 on 2023-09-21 14:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0031_alter_image_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='size_in_persons',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='studio',
            name='size_in_persons',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(0)]),
        ),
    ]
