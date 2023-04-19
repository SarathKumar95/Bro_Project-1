# Generated by Django 4.1.4 on 2023-04-19 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0112_productvariant_is_base_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="product_color",
            name="is_base_color",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="products",
            name="base_price",
            field=models.FloatField(default=0),
        ),
    ]
