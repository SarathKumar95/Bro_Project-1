# Generated by Django 4.1.3 on 2022-11-24 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0016_products_second_image_products_third_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('sub_cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_type_image', models.ImageField(blank=True, null=True, upload_to='images/producttype')),
                ('product_type', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'verbose_name_plural': 'SubCategories',
            },
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name_plural': 'Products'},
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='category_image',
            new_name='category_img',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='category_name',
        ),
        migrations.RemoveField(
            model_name='products',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='products',
            name='category',
        ),
        migrations.RemoveField(
            model_name='products',
            name='description',
        ),
        migrations.AddField(
            model_name='categories',
            name='condition',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='battery',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='camera',
            field=models.CharField(default='12 MP', max_length=100),
        ),
        migrations.AddField(
            model_name='products',
            name='ram',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='screen_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='color',
            field=models.CharField(default='white', max_length=20),
        ),
        migrations.AlterField(
            model_name='products',
            name='condition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.categories'),
        ),
        migrations.AlterField(
            model_name='products',
            name='generation',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='internal_storage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='products',
            name='series',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='product_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.producttype'),
        ),
        migrations.AddField(
            model_name='products',
            name='product_type',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='category.producttype'),
        ),
    ]
