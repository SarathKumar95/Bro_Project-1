# Generated by Django 4.1.3 on 2022-12-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0054_coupon_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
