# Generated by Django 4.1.3 on 2022-12-12 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0041_producttype_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
