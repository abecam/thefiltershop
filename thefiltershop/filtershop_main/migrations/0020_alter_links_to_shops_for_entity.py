# Generated by Django 4.2.1 on 2023-09-12 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0019_alter_entity_vignette'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links_to_shops',
            name='for_Entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filtershop_main.entity'),
        ),
    ]