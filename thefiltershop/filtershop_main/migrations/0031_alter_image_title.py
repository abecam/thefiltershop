# Generated by Django 4.2.1 on 2023-09-21 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0030_alter_image_options_alter_links_to_shops_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
