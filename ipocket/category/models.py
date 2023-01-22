from django.db import models

from accounts.models import MyUser
from django.utils.timezone import now

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


# product model
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    condition = models.ForeignKey(
        Categories, on_delete=models.CASCADE, null=True)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, default=True)
    generation = models.IntegerField(null=True, blank=True)
    series = models.CharField(max_length=25, null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    internal_storage = models.IntegerField(null=True, blank=True)
    processor = models.CharField(max_length=25, null=True, blank=True)
    battery = models.CharField(max_length=20, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    screen_size = models.DecimalField(
        decimal_places=2, max_digits=4, null=True, blank=True)
    camera = models.CharField(
        max_length=100, default='12 MP', null=True, blank=True)
    color = models.CharField(max_length=20, default='White')
    #total_quantity = models.IntegerField(default=0)
    slug = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    main_image = models.ImageField(
        upload_to='images/products', null=True, blank=True) 
    price = models.FloatField(default=100)    
         
    
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return '{} - {} - {}'.format(self.product_name, self.generation, self.series)




class ProductAttribute(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE,default=1)
    size = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0) 
    color = models.CharField(max_length=100,default='black')
    first_image = models.ImageField(
        upload_to='images/products', null=True, blank=True)
    second_image = models.ImageField(
        upload_to='images/products', null=True, blank=True)
    third_image = models.ImageField(
        upload_to='images/products', null=True, blank=True)
    product_offer = models.IntegerField(null=True, blank=True) 
    applied_offer = models.CharField(max_length=100, null=True,blank=True)
    price_after_offer = models.FloatField(null=True,blank=True)
    slug = models.CharField(max_length=100,null=True,blank=True)   
    is_featured=models.BooleanField(default=False)



    def __str__(self):
        return self.slug

    
    def save(self, *args, **kwargs):

        #need to fetch product id to assign a common price to the product depending on which is lower 

        pro_id = self.product.product_id 

        #check all product attribute belonging to that product 

        product_price = ProductAttribute.objects.filter(product_id=pro_id).order_by('-price')
        product_offer_price = ProductAttribute.objects.filter(product_id=pro_id).order_by('-price_after_offer') 

        print("Check ", product_offer_price)

        # if self.price_after_offer == 0 or None:
        #     pass

        # else:
        #     if product_offer_price.last().price_after_offer < product_price.last().price:
        #         self.product.price = product_offer_price.last().price_after_offer

        #     elif product_offer_price.last().price_after_offer > product_price.last().price:
        #         self.product.price = product_price.last().price             

     
        # self.product.save()

        # if self.product.product_type.offer_percentage == None and self.product_offer != None:
            
        #     Price_on_Offer = (self.price * self.product_offer)/100     
        #     price_after_productoffer = self.price - Price_on_Offer
        #     self.price_after_offer=price_after_productoffer 
        #     self.applied_offer="Product Offer"

        
        # elif self.product.product_type.offer_percentage != None and self.product_offer == None:
            
        #     Price_on_Offer = (self.price * self.product.product_type.offer_percentage)/100     
        #     price_after_categoryoffer = self.price - Price_on_Offer
        #     self.price_after_offer=price_after_categoryoffer 
        #     self.applied_offer="Category Offer"
        #     print("Price after product offer is", price_after_categoryoffer) 

        # elif self.product.product_type.offer_percentage != None and self.product_offer != None:

    
        #     Price_on_Offer = (self.price * self.product_offer)/100

        #     Price_on_categoryOffer=(self.price * self.product.product_type.offer_percentage)/100 

        #     price_after_productoffer = self.price - Price_on_Offer
        #     price_after_categoryoffer = self.price - Price_on_categoryOffer
            
            
        #     if price_after_productoffer < price_after_categoryoffer:
        #         self.price_after_offer=price_after_productoffer 
        #         self.applied_offer="Product Offer"

        #     elif price_after_categoryoffer < price_after_productoffer:     
        #         self.price_after_offer=price_after_categoryoffer
        #         self.applied_offer="Category Offer"
        #     elif price_after_categoryoffer == price_after_productoffer:
        #         self.price_after_offer=price_after_categoryoffer
        #         self.applied_offer="Both Offer are Same" 
            
        # else:
        #     self.price_after_offer=0
        #     self.applied_offer=''       
            

        super(ProductAttribute, self).save(*args, **kwargs)
    



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
    product = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
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
    wishlist_name=models.CharField(max_length=100,null=True,blank=True) 
      
    def __str__(self):

        if self.wishlist_name != None:

            return '{}' - '{}'.format(self.user.email, self.wishlist_name) 

        else:
            return self.user.email    

#wallet
class Wallet(models.Model):
    wallet_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE) 
    orderItem=models.ForeignKey(OrderItem,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField(null=True,blank=True)
    amount=models.FloatField(null=True,blank=True) 

    def __str__(self):
        return '{}'.format(str(self.wallet_id)) 

class Banner(models.Model):
    banner_id = models.AutoField(primary_key=True)
    banner_name = models.CharField(max_length=100,null=True,blank=True)
    banner_image = models.ImageField(null=True,blank=True)
    banner_head = models.CharField(max_length=150,null=True,blank=True)
    banner_link = models.CharField(max_length=150,null=True,blank=True) 

    def __str__(self):
        return '{}'.format((self.banner_name))
