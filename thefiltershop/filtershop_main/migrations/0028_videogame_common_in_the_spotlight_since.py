# Generated by Django 4.2.1 on 2023-09-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0027_videogame_common_in_the_spotlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='videogame_common',
            name='in_the_spotlight_since',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]