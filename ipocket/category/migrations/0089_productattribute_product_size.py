# Generated by Django 4.1.4 on 2023-04-14 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0088_remove_productattribute_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="productattribute",
            name="product_size",
            field=models.IntegerField(default=0),
        ),
    ]