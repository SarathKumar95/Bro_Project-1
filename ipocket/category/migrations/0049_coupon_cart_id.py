# Generated by Django 4.1.3 on 2022-12-15 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0048_remove_coupon_tries'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='cart_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
