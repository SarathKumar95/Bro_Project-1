# Generated by Django 4.1.3 on 2022-12-23 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0066_remove_order_tax_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price_before_tax',
        ),
    ]