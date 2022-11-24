# Generated by Django 4.1.3 on 2022-11-24 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0020_alter_products_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='camera',
            field=models.CharField(blank=True, default='12 MP', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='generation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]