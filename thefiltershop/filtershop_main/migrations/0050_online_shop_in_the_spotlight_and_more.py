# Generated by Django 4.2.1 on 2023-10-12 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0049_alter_online_shop_they_have_made_it_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='online_shop',
            name='in_the_spotlight',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='online_shop',
            name='in_the_spotlight_since',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='physical_shop',
            name='in_the_spotlight',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='physical_shop',
            name='in_the_spotlight_since',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='software',
            name='in_the_spotlight',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='in_the_spotlight_since',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]