# Generated by Django 4.1.3 on 2022-11-22 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0062_categories_category_img'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubCategories',
            new_name='ProductType',
        ),
    ]
