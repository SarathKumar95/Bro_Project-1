# Generated by Django 4.1.3 on 2022-12-15 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0050_remove_coupon_cart_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='grand_total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]