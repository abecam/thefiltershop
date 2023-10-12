# Generated by Django 4.2.1 on 2023-10-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0054_videogame_rating_same_platform_alternative_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogame_rating',
            name='same_platform_alternative_shop',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='If on the same platform but for a different shop with different conditions (i.e. F2P instead of premium), give the name of the shop'),
        ),
    ]
