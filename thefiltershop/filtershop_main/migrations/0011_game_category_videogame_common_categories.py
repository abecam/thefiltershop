# Generated by Django 4.2.1 on 2023-08-31 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0010_entry_on_steam'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date creation')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related_type', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'ordering': ['date_creation', 'name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='videogame_common',
            name='categories',
            field=models.ManyToManyField(to='filtershop_main.game_category'),
        ),
    ]
