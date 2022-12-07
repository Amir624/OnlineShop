# Generated by Django 4.1.3 on 2022-12-01 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('discount', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]