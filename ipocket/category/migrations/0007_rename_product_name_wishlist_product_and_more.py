# Generated by Django 4.1.4 on 2023-05-04 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0006_wishlist"),
    ]

    operations = [
        migrations.RenameField(
            model_name="wishlist",
            old_name="product_name",
            new_name="product",
        ),
        migrations.RemoveField(
            model_name="wishlist",
            name="variant_color",
        ),
        migrations.AddField(
            model_name="wishlist",
            name="base_color",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="color_selected",
                to="category.product_color",
            ),
        ),
        migrations.AddField(
            model_name="wishlist",
            name="base_variant",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="variant_selected",
                to="category.productvariant",
            ),
        ),
    ]
