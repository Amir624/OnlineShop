# Generated by Django 4.1.3 on 2022-11-21 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='color',
            field=models.ManyToManyField(blank=True, related_name='var_color', to='products.color'),
        ),
    ]
