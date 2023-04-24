# Generated by Django 4.1.4 on 2023-04-24 06:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                ("banner_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "banner_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "banner_image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                (
                    "banner_head",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                (
                    "banner_link",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                ("coupon_id", models.AutoField(primary_key=True, serialize=False)),
                ("coupon_code", models.CharField(max_length=100, unique=True)),
                ("valid_till", models.DateField(default=django.utils.timezone.now)),
                ("is_expired", models.BooleanField(default=False)),
                ("one_time_use", models.BooleanField(default=False)),
                ("discount_percentage", models.IntegerField()),
                ("minimum_amount", models.IntegerField()),
                ("maximum_amount", models.IntegerField(default=90000)),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(max_length=150, null=True)),
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                ("email", models.CharField(max_length=150)),
                ("phone", models.BigIntegerField()),
                ("address", models.TextField(max_length=200, null=True)),
                ("state", models.CharField(max_length=100, null=True)),
                ("city", models.CharField(max_length=100, null=True)),
                ("pincode", models.IntegerField(null=True)),
                ("total_price", models.FloatField(null=True)),
                ("ship_amount", models.FloatField(null=True)),
                ("coupon_amount", models.FloatField(null=True)),
                ("payment_mode", models.CharField(max_length=150, null=True)),
                ("payment_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Order Confirmed", "Order Confirmed"),
                            ("Shipped", "Shipped"),
                            ("In Transit", "In Transit"),
                            ("Out for Delivery", "Out for Delivery"),
                            ("Delivered", "Delivered"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Order Confirmed",
                        max_length=150,
                    ),
                ),
                ("message", models.TextField(blank=True, null=True)),
                ("tracking_no", models.CharField(max_length=150, null=True)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("coupon", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product_Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color_name", models.CharField(max_length=50)),
                ("color_price", models.FloatField(blank=True, default=0, null=True)),
                ("image1", models.ImageField(blank=True, upload_to="color_images")),
                ("image2", models.ImageField(blank=True, upload_to="color_images")),
                ("image3", models.ImageField(blank=True, upload_to="color_images")),
                ("is_base_color", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Products",
            fields=[
                ("product_id", models.AutoField(primary_key=True, serialize=False)),
                ("product_name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("main_image", models.ImageField(blank=True, upload_to="products")),
                ("second_image", models.ImageField(blank=True, upload_to="products")),
                ("third_image", models.ImageField(blank=True, upload_to="products")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("available", models.BooleanField(default=True)),
                ("total_quantity", models.IntegerField(blank=True, null=True)),
                ("price_after_offer", models.FloatField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("os", models.CharField(blank=True, max_length=50)),
                ("display", models.CharField(blank=True, max_length=50)),
                ("camera", models.CharField(blank=True, max_length=50)),
                ("battery", models.CharField(blank=True, max_length=50)),
                ("os_version", models.CharField(blank=True, max_length=50)),
                ("case_material", models.CharField(blank=True, max_length=50)),
                ("band_material", models.CharField(blank=True, max_length=50)),
                ("water_resistance", models.CharField(blank=True, max_length=50)),
                ("size", models.CharField(blank=True, max_length=50)),
                ("compatibility", models.CharField(blank=True, max_length=50)),
                ("battery_life", models.CharField(blank=True, max_length=50)),
                ("noise_cancellation", models.BooleanField(default=False)),
                ("wireless_charging", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                ("sub_cat_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "product_type_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="images/producttype"
                    ),
                ),
                ("product_type", models.CharField(max_length=25, unique=True)),
                ("offer_percentage", models.IntegerField(blank=True, null=True)),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "SubCategories",
            },
        ),
        migrations.CreateModel(
            name="ProductVariant",
            fields=[
                (
                    "product_variant_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("variant_name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_base_variant", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="category.products",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VariantColor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.product_color",
                    ),
                ),
                (
                    "variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.productvariant",
                    ),
                ),
            ],
            options={
                "unique_together": {("variant", "color")},
            },
        ),
        migrations.AddField(
            model_name="products",
            name="product_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="category.producttype"
            ),
        ),
        migrations.AddField(
            model_name="product_color",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="colors",
                to="category.products",
            ),
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.FloatField(null=True)),
                ("quantity", models.IntegerField(null=True)),
                (
                    "item_status",
                    models.CharField(
                        choices=[
                            ("Order Confirmed", "Order Confirmed"),
                            ("Shipped", "Shipped"),
                            ("In Transit", "In Transit"),
                            ("Out for Delivery", "Out for Delivery"),
                            ("Delivered", "Delivered"),
                        ],
                        default="Order Confirmed",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="category.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.products",
                    ),
                ),
                (
                    "variantColor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variantColor_selected",
                        to="category.variantcolor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Categories",
            fields=[
                ("category_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "category_img",
                    models.ImageField(
                        blank=True, null=True, upload_to="images/categories"
                    ),
                ),
                ("condition", models.CharField(max_length=25, null=True)),
                ("slug", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "product_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.producttype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
    ]