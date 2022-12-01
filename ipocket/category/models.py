from django.db import models

from accounts.models import MyUser

# Create your models here.

#sub category on phones/watches/airpods 

class ProductType(models.Model):
    sub_cat_id = models.AutoField(primary_key=True) 
    product_type_image = models.ImageField(upload_to='images/producttype',null=True,blank=True)
    product_type = models.CharField(max_length=25,unique=True)

    class Meta:
        verbose_name_plural = 'SubCategories'


    def __str__(self):
        return self.product_type    



#category on new/old 

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_img = models.ImageField(upload_to='images/categories',null=True,blank=True)
    condition = models.CharField(max_length=25,null=True) 
    product_type = models.ForeignKey(ProductType,on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.condition    





# product model
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    condition = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    product_type = models.ForeignKey(ProductType,on_delete=models.CASCADE,default=True)
    generation = models.IntegerField(null=True,blank=True)
    series = models.CharField(max_length=25, null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True) 
    internal_storage = models.IntegerField(null=True,blank=True)
    processor = models.CharField(max_length=25,null=True,blank=True)
    battery=models.CharField(max_length=20,null=True,blank=True)
    weight=models.IntegerField(null=True,blank=True)
    screen_size = models.DecimalField(decimal_places=2,max_digits=4,null=True,blank=True)
    camera = models.CharField(max_length=100,default='12 MP',null=True,blank=True)
    color = models.CharField(max_length=20,default='white')
    price = models.IntegerField(default=100) 
    quantity = models.IntegerField(default=0)
    main_image = models.ImageField(upload_to='images/products',null=True,blank=True) 
    second_image = models.ImageField(upload_to='images/products',null=True,blank=True) 
    third_image = models.ImageField(upload_to='images/products',null=True,blank=True)  


    class Meta:
        verbose_name_plural = 'Products' 

    def __str__(self):
        return self.product_name 


class Order(models.Model):
    user = models.CharField(max_length=150,null=True)
    first_name = models.CharField(max_length=150,null=False) 
    last_name = models.CharField(max_length=150,null=False) 
    email = models.CharField(max_length=150,null=False) 
    phone = models.BigIntegerField()
    address_line1 = models.TextField(max_length=200,null=True)
    address_line2 = models.TextField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    pincode = models.IntegerField(null=True)
    total_price = models.FloatField(null=True)
    tax_amount = models.FloatField(null=True)
    ship_amount = models.FloatField(null=True)
    coupon_amount = models.FloatField(null=True)
    payment_mode = models.CharField(max_length=150,null=True)
    price_before_tax = models.FloatField(null=True)
    payment_id = models.CharField(max_length=255,null=True,blank=True)
    orderstatus = [
        ('Order Placed','Order Placed'),
        ('Order Confirmed','Order Confirmed'),
        ('Pending','Pending'),
        ('Shipped','Shipped'),
        ('In Transit','In Transit'),
        ('Completed','Completed'),
        ('Awaiting Payment','Awaiting Payment'),
        ('Out for Delivery','Out for Delivery'),
        ('Cancelled','Cancelled'),
    ]
    status = models.CharField(max_length=150,choices=orderstatus,default='Order Placed')
    message = models.TextField(null=True,blank=True)
    tracking_no = models.CharField(max_length=150,null=True)
    #tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True) 


    def __str__(self):
        return '{} - {}'.format(self.user,str(self.tracking_no) )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True) 
    item_status = models.CharField(null=True,blank=True)

    def __str__(self):
        return '{} - {}'.format(self.order.user,self.order.tracking_no)