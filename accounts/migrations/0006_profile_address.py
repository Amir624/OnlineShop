# Generated by Django 4.1.3 on 2022-12-04 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]