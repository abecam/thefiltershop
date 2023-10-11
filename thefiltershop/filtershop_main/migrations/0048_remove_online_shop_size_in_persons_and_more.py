# Generated by Django 4.2.1 on 2023-10-11 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0047_physical_shop_size_of_shop_sponsor_size_of_shop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='online_shop',
            name='size_in_persons',
        ),
        migrations.RemoveField(
            model_name='physical_shop',
            name='size_in_persons',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='size_of_shop',
        ),
        migrations.AddField(
            model_name='online_shop',
            name='size_of_shop',
            field=models.CharField(choices=[('AR', 'Artisan (5 persons or less)'), ('IN', 'Indie (>5 persons, less than 20)'), ('ME', 'Medium (>20, less than 50)'), ('BI', 'Big (>50 less than 200)'), ('HU', 'Huge (>200)')], default='AR', max_length=2),
        ),
    ]
