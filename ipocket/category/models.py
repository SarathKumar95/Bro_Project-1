from django.db import models

# Create your models here.


# category based on conditions eg:- new and old
class Category(models.Model):
    category_id = models.AutoField(primary_key=True) 
    category_name = models.CharField(max_length=50,unique=True) 

    class Meta:
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.category_name     


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50) 
    condition = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
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