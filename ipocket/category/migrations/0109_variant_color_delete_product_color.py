# Generated by Django 4.1.4 on 2023-04-19 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0108_remove_productvariant_variant_color_product_color"),
    ]

    operations = [
        migrations.CreateModel(
            name="Variant_Color",
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
                ("color_name", models.CharField(default="Black", max_length=10)),
                ("price_increase", models.IntegerField(default=0)),
                ("quantity", models.IntegerField(default=0)),
                (
                    "product_variant",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.productvariant",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Product_Color",
        ),
    ]
