# Generated by Django 4.1.3 on 2022-11-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
