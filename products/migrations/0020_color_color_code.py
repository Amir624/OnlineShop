# Generated by Django 4.1.3 on 2022-11-28 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_remove_variant_color_remove_variant_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='color_code',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]