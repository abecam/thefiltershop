# Generated by Django 4.2.1 on 2023-10-06 18:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0040_alter_typeofentity_filters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physical_shop',
            name='ethical_rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
