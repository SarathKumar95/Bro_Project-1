# Generated by Django 4.1.4 on 2023-04-21 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0020_alter_cart_color_selected_alter_cart_product_attr_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="color_selected",
        ),
        migrations.RemoveField(
            model_name="cart",
            name="variant_selected",
        ),
    ]
