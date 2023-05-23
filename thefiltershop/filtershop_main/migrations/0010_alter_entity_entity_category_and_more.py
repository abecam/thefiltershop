# Generated by Django 4.2.1 on 2023-05-19 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filtershop_main', '0009_alter_videogame_common_spotlight_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='Entity_Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='filtershop_main.entity_category'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='Links_to_shops',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='filtershop_main.links_to_shops'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='parent_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filtershop_main.tag'),
        ),
    ]