from django.db import models
from image_cropping import ImageRatioField
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
    condition = models.CharField(max_length=25) 
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
    generation = models.IntegerField(null=True)
    series = models.CharField(max_length=25, null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True) 
    internal_storage = models.IntegerField(null=True,blank=True)
    screen_size = models.DecimalField(decimal_places=2,max_digits=4,null=True,blank=True)
    camera = models.CharField(max_length=100,default='12 MP')
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