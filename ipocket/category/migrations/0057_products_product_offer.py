# Generated by Django 4.1.3 on 2022-12-20 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0056_producttype_offer_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_offer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
