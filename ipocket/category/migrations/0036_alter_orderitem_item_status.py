# Generated by Django 4.1.3 on 2022-12-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0035_alter_orderitem_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_status',
            field=models.CharField(choices=[('Order Placed', 'Order Placed'), ('Order Confirmed', 'Order Confirmed'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('In Transit', 'In Transit'), ('Completed', 'Completed'), ('Awaiting Payment', 'Awaiting Payment'), ('Out for Delivery', 'Out for Delivery'), ('Cancelled', 'Cancelled')], default='Order Placed', max_length=50, null=True),
        ),
    ]
