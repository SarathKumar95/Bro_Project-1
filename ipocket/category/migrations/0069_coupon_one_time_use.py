# Generated by Django 4.1.4 on 2022-12-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0068_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="one_time_use",
            field=models.BooleanField(default=False),
        ),
    ]
