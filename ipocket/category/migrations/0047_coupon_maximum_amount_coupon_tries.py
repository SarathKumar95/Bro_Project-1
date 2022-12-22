# Generated by Django 4.1.3 on 2022-12-14 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0046_coupon_valid_till'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='maximum_amount',
            field=models.IntegerField(default=90000),
        ),
        migrations.AddField(
            model_name='coupon',
            name='tries',
            field=models.IntegerField(default=1),
        ),
    ]