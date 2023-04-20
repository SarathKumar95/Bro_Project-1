# Generated by Django 4.1.4 on 2023-04-20 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0114_productvariant_variant_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productvariant",
            name="product",
        ),
        migrations.AddField(
            model_name="products",
            name="color",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="color_price",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="products",
            name="variant",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="products",
            name="variant_price",
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name="Product_Color",
        ),
        migrations.DeleteModel(
            name="ProductVariant",
        ),
    ]
