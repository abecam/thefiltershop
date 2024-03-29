# Generated by Django 4.2.1 on 2023-10-05 12:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0034_typeofrelationbetweenfilter_reverse_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiltersForAVideoGameRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date creation')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('value', models.IntegerField(default=50, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_related_type', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filtershop_main.filter')),
                ('for_rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filtershop_main.videogame_rating')),
            ],
            options={
                'ordering': ['date_creation', 'name'],
                'abstract': False,
            },
        ),
    ]
