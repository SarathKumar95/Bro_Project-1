# Generated by Django 4.1.3 on 2022-11-21 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0058_products_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='product_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.subcategories'),
        ),
    ]
