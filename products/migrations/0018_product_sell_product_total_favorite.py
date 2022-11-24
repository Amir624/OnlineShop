# Generated by Django 4.1.3 on 2022-11-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='total_favorite',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
