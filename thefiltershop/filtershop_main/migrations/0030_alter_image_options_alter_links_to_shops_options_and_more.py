# Generated by Django 4.2.1 on 2023-09-21 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0029_entity_headline'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={},
        ),
        migrations.AlterModelOptions(
            name='links_to_shops',
            options={},
        ),
        migrations.RemoveField(
            model_name='image',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='image',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='image',
            name='description',
        ),
        migrations.RemoveField(
            model_name='image',
            name='last_update',
        ),
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
        migrations.RemoveField(
            model_name='links_to_shops',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='links_to_shops',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='links_to_shops',
            name='description',
        ),
        migrations.RemoveField(
            model_name='links_to_shops',
            name='last_update',
        ),
        migrations.RemoveField(
            model_name='links_to_shops',
            name='name',
        ),
    ]
