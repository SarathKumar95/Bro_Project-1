# Generated by Django 4.1.4 on 2023-04-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0105_alter_product_color_color_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product_color",
            name="color_name",
            field=models.CharField(default="Black", max_length=10),
        ),
    ]