# Generated by Django 4.1.3 on 2022-12-22 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0063_rename_user_wishlist_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='user_id',
            new_name='user',
        ),
    ]