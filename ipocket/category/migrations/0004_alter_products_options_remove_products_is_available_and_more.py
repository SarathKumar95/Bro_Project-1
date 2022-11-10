# Generated by Django 4.1.1 on 2022-11-10 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_products_description_products_images_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.RemoveField(
            model_name='products',
            name='is_available',
        ),
        migrations.AddField(
            model_name='products',
            name='internal_storage',
            field=models.CharField(default='32 GB', max_length=5),
        ),
        migrations.AlterField(
            model_name='products',
            name='series',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]