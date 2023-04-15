# Generated by Django 4.1.4 on 2023-04-15 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0101_product_color_color_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product_color",
            name="product_variant",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="category.productvariant",
            ),
        ),
    ]
