# Generated by Django 4.1.4 on 2023-04-14 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "category",
            "0098_product_subvariant_rename_price_products_base_price_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Product_Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Product_SubVariant",
        ),
        migrations.RemoveField(
            model_name="products",
            name="internal_storage",
        ),
    ]