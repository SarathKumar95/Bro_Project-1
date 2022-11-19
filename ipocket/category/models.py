from django.db import models

# Create your models here.


#product spec model 
class Product_Spec(models.Model):
    generation = models.IntegerField(default=11) 
    series = models.CharField(max_length=50,blank=True) 
    ram = models.IntegerField(default=4,blank=True) 
    internal_memory = models.IntegerField(default=32,blank=True) 
    screen_size = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
    type_of_display = models.CharField(max_length=100,blank=True)
    processor = models.CharField(max_length=100,blank=True)
    camera_spec = models.IntegerField(default=12,blank=True) 
    
    class Meta:
        verbose_name_plural = 'Product Specifications' 

    def __str__(self):
        return str(self.generation) + self.series    



# sub category based on the device generation and series 
class SubCategory(models.Model):
    sub_category_id = models.AutoField(primary_key=True) 
    product_type = models.CharField(max_length=50,unique=True) 
    
    
    class Meta:
        verbose_name_plural = 'Sub Categories' 

    def __str__(self):
        return self.product_type    


# category based on conditions eg:- new and old
class Category(models.Model):
    category_id = models.AutoField(primary_key=True) 
    category_name = models.CharField(max_length=50,unique=True) 
    
    
    class Meta:
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.category_name



# product model
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_type = models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=True)
    condition = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    generation = models.ForeignKey(Product_Spec,on_delete=models.CASCADE,null=True)
    price = models.IntegerField() 
    quantity = models.IntegerField()
    description = models.TextField(max_length=500,blank=True) 
    main_image = models.ImageField(upload_to='images/products',null=True,blank=True) 
    second_image = models.ImageField(upload_to='images/products',null=True,blank=True) 
    third_image = models.ImageField(upload_to='images/products',null=True,blank=True)  

    class Meta:
        verbose_name_plural = 'Products' 

    def __str__(self):
        return self.product_name