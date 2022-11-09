from django.db import models

# Create your models here.

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length = 50, unique =True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name        


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    generation = models.IntegerField()
    series = models.CharField(max_length=10)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.IntegerField(default=1000)
    quantity = models.IntegerField(default=0)
    description = models.TextField(max_length=500, null=True, blank=True)
    images = models.ImageField(upload_to = 'images/products',null=True, blank=True)
    is_available = models.BooleanField(default=True,null=True)
    is_out_of_stock = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def __str__(self):
        return self.product_name + str(self.generation) + self.series

