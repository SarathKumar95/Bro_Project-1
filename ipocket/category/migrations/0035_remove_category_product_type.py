# Generated by Django 4.1.3 on 2022-11-19 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0034_category_product_type_alter_subcategory_product_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='product_type',
        ),
    ]
