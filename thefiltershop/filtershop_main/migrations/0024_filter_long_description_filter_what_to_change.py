# Generated by Django 4.2.1 on 2023-09-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0023_alter_entity_tags_alter_online_shop_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='long_description',
            field=models.TextField(blank=True, max_length=20000, null=True),
        ),
        migrations.AddField(
            model_name='filter',
            name='what_to_change',
            field=models.TextField(blank=True, max_length=20000, null=True),
        ),
    ]
