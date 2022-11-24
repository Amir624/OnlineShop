# Generated by Django 4.1.3 on 2022-11-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_alter_product_color_alter_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='size',
        ),
        migrations.AddField(
            model_name='variant',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='var_size', to='products.size'),
        ),
    ]