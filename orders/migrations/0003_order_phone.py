# Generated by Django 4.1.3 on 2022-11-30 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_note_alter_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]