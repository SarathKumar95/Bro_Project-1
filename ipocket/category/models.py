from django.db import models

# Create your models here.

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_image = models.ImageField(upload_to='images/categories', null=True, blank=True)
    category_name = models.CharField(max_length = 50, unique =True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name        


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    generation = models.IntegerField(blank=True,null=True)
    series = models.CharField(max_length=10,blank=True)
    color = models.CharField(max_length=10,null=True,blank=True)
    internal_storage = models.CharField(max_length=5, default= '32 GB')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.IntegerField(default=1000)
    quantity = models.IntegerField(default=0)
    condition = models.CharField(max_length=30,null=True,blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    images = models.ImageField(upload_to = 'images/products',null=True, blank=True)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    
    def __str__(self):
        return self.product_name + str(self.generation) + self.series

    