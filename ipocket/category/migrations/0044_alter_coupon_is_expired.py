# Generated by Django 4.1.3 on 2022-12-14 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0043_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]