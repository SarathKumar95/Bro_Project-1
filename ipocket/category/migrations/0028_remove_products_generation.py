# Generated by Django 4.1.3 on 2022-11-19 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0027_products_generation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='generation',
        ),
    ]
