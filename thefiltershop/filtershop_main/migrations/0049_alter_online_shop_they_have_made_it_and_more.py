# Generated by Django 4.2.1 on 2023-10-12 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0048_remove_online_shop_size_in_persons_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='online_shop',
            name='they_have_made_it',
            field=models.CharField(choices=[('NO', 'Not yet'), ('YE', 'Yes'), ('ME', 'Yes, and we helped a bit'), ('MA', 'Yes, mostly thanks to us! Great!')], default='NO', max_length=2),
        ),
        migrations.AlterField(
            model_name='physical_shop',
            name='they_have_made_it',
            field=models.CharField(choices=[('NO', 'Not yet'), ('YE', 'Yes'), ('ME', 'Yes, and we helped a bit'), ('MA', 'Yes, mostly thanks to us! Great!')], default='NO', max_length=2),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='they_have_made_it',
            field=models.CharField(choices=[('NO', 'Not yet'), ('YE', 'Yes'), ('ME', 'Yes, and we helped a bit'), ('MA', 'Yes, mostly thanks to us! Great!')], default='NO', max_length=2),
        ),
        migrations.AlterField(
            model_name='software',
            name='they_have_made_it',
            field=models.CharField(choices=[('NO', 'Not yet'), ('YE', 'Yes'), ('ME', 'Yes, and we helped a bit'), ('MA', 'Yes, mostly thanks to us! Great!')], default='NO', max_length=2),
        ),
        migrations.AlterField(
            model_name='studio',
            name='they_have_made_it',
            field=models.CharField(choices=[('NO', 'Not yet'), ('YE', 'Yes'), ('ME', 'Yes, and we helped a bit'), ('MA', 'Yes, mostly thanks to us! Great!')], default='NO', max_length=2),
        ),
        migrations.AlterField(
            model_name='videogame_common',
            name='they_have_made_it',
            field=models.CharField(choices=[('NO', 'Not yet'), ('YE', 'Yes'), ('ME', 'Yes, and we helped a bit'), ('MA', 'Yes, mostly thanks to us! Great!')], default='NO', max_length=2),
        ),
    ]
