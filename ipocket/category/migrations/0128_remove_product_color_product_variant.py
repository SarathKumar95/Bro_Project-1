# Generated by Django 4.1.4 on 2023-04-20 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0127_product_color_color_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product_color",
            name="product_variant",
        ),
    ]
