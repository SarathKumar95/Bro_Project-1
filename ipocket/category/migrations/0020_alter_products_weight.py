# Generated by Django 4.1.3 on 2022-11-24 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0019_alter_products_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]
