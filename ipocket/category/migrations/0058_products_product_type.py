# Generated by Django 4.1.3 on 2022-11-21 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0057_subcategories'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_type',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='category.subcategories'),
        ),
    ]
