# Generated by Django 4.1.3 on 2022-11-21 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0054_delete_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('condition', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
