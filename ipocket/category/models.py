from django.db import models

from accounts.models import MyUser
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

# Create your models here.

# sub category on phones/watches/airpods


class ProductType(models.Model):
    sub_cat_id = models.AutoField(primary_key=True)
    product_type_image = models.ImageField(
        upload_to='images/producttype', null=True, blank=True)
    product_type = models.CharField(max_length=25, unique=True)
    offer_percentage = models.IntegerField(null=True, blank=True)
    slug = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.product_type

    
    def save(self,*args,**kwargs):
        product=Products.objects.filter(product_type=self.sub_cat_id)
        
        for item in product:
            price = item.price    

            if self.offer_percentage != None:
            
                Price_on_categoryOffer=(price * self.offer_percentage)/100
                price_after_categoryoffer = price - Price_on_categoryOffer 
                item.price_after_offer=price_after_categoryoffer 

                print("Price before category offer is", price) 
                print("Price after category offer is", item.price_after_offer) 

                

            else:
                item.price_after_offer = None   

                
                print("Price before category offer is", price)
                print("Price after category offer is", item.price_after_offer)
            
            item.save()

        super(ProductType, self).save(*args, **kwargs)

            


# category on new/old

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_img = models.ImageField(
        upload_to='images/categories', null=True, blank=True)
    condition = models.CharField(max_length=25, null=True)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, null=True)
    slug = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.condition


# # product model
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, unique=True)
    product_type = models.ForeignKey(ProductType,on_delete=models.CASCADE)

    description = models.TextField(null=True,blank=True)
    main_image = models.ImageField(upload_to='products', blank=True)
    second_image = models.ImageField(upload_to='products', blank=True)
    third_image = models.ImageField(upload_to='products', blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    
    total_quantity = models.IntegerField(null=True,blank=True)
    price_after_offer = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # iPhone-specific fields
    os = models.CharField(max_length=50, blank=True)
    display = models.CharField(max_length=50, blank=True)
    #storage = models.CharField(max_length=50, blank=True)
    camera = models.CharField(max_length=50, blank=True)
    battery = models.CharField(max_length=50, blank=True)
    
    # Watch-specific fields
    os_version = models.CharField(max_length=50, blank=True)
    case_material = models.CharField(max_length=50, blank=True)
    band_material = models.CharField(max_length=50, blank=True)
    water_resistance = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    
    # AirPods-specific fields
    compatibility = models.CharField(max_length=50, blank=True)
    battery_life = models.CharField(max_length=50, blank=True)
    noise_cancellation = models.BooleanField(default=False)
    wireless_charging = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return '{}'.format(self.product_name) 


class ProductVariant(models.Model):
    product_variant_id = models.AutoField(primary_key=True)
    variant_name = models.CharField(max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    is_base_variant = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.product.product_name,self.variant_name) 

class Product_Color(models.Model):
    color_name = models.CharField(max_length=50)
    color_price = models.FloatField(null=True,blank=True,default=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='colors')
    #product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='variant_colors',null=True,blank=True)
    image1 = models.ImageField(upload_to='color_images', blank=True)
    image2 = models.ImageField(upload_to='color_images', blank=True)
    image3 = models.ImageField(upload_to='color_images', blank=True)
    is_base_color = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.product.product_name,self.color_name) 

class VariantColor(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    color = models.ForeignKey(Product_Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0) 

    def save(self,*args,**kwargs):
        productId = self.variant.product.product_id 
        product = Products.objects.get(product_id = productId) 

        product.total_quantity += self.quantity  
        product.save()

        super(VariantColor,self).save(*args,**kwargs) 

    class Meta:
        unique_together = ('variant', 'color')

    def __str__(self):
        return "{} - {} ({})".format(self.variant.product.product_name, self.variant.variant_name, self.color.color_name)


class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_code = models.CharField(max_length=100, unique=True)
    valid_till = models.DateField(default=now)
    is_expired = models.BooleanField(default=False)
    one_time_use = models.BooleanField(default=False)
    discount_percentage = models.IntegerField()
    minimum_amount = models.IntegerField()
    maximum_amount = models.IntegerField(default=90000)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.coupon_code)

    def save(self, *args, **kwargs):
        today = datetime.date.today()

        print("Valid till is", self.valid_till)
        print("Todays date is", today)

        if self.valid_till < today:
            print("Date has passed", self.is_expired)

            self.is_expired = True

        else:
            print("Date is coming..", self.is_expired)
            self.is_expired = False
        super(Coupon, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.CharField(max_length=150, null=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.BigIntegerField()
    address = models.TextField(max_length=200, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    pincode = models.IntegerField(null=True)
    total_price = models.FloatField(null=True)
    ship_amount = models.FloatField(null=True)
    coupon_amount = models.FloatField(null=True)
    payment_mode = models.CharField(max_length=150, null=True)
    #price_before_tax = models.FloatField(null=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    orderstatus = [
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', 'Shipped'),
        ('In Transit', 'In Transit'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered','Delivered'),
        ('Cancelled', 'Cancelled'),
        
    ]
    status = models.CharField(
        max_length=150, choices=orderstatus, default='Order Confirmed')
    message = models.TextField(null=True, blank=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    coupon = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.user, str(self.tracking_no))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE) 
    variantColor = models.ForeignKey(VariantColor,on_delete=models.CASCADE,related_name='variantColor_selected')
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)
    order_itemstatus = [
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', 'Shipped'),
        ('In Transit', 'In Transit'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        
    ]
    item_status = models.CharField(
        max_length=50, choices=order_itemstatus, default="Order Confirmed", null=True)

    def __str__(self):
        return '{} - {}'.format(self.order.user, self.order.tracking_no)


class Wishlist(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True) 
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    variant=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    color=models.ForeignKey(Product_Color,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email    

# #wallet
# class Wallet(models.Model):
#     wallet_id=models.AutoField(primary_key=True)
#     user=models.ForeignKey(MyUser,on_delete=models.CASCADE) 
#     orderItem=models.ForeignKey(OrderItem,on_delete=models.CASCADE,null=True,blank=True)
#     quantity=models.IntegerField(null=True,blank=True)
#     amount=models.FloatField(null=True,blank=True) 

#     def __str__(self):
#         return '{}'.format(str(self.wallet_id)) 

class Banner(models.Model):
    banner_id = models.AutoField(primary_key=True)
    banner_name = models.CharField(max_length=100,null=True,blank=True)
    banner_image = models.ImageField(null=True,blank=True)
    banner_head = models.CharField(max_length=150,null=True,blank=True)
    banner_link = models.CharField(max_length=150,null=True,blank=True) 

    def __str__(self):
        return '{}'.format((self.banner_name))
