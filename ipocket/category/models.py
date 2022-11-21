from django.db import models

# Create your models here.

#sub category on phones/watches/airpods 

class SubCategories(models.Model):
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
    condition = models.CharField(max_length=25) 
    product_type = models.ForeignKey(SubCategories,on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name_plural = 'Categories' 

    def __str__(self):
        return self.condition    





# product model
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    condition = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    product_type = models.ForeignKey(SubCategories,on_delete=models.CASCADE,default=True)
    #generation = models.ForeignKey(Product_Spec,on_delete=models.CASCADE,null=True)
    # series = models.ForeignKey(Product_Spec, on_delete=models.CASCADE,null=True)
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