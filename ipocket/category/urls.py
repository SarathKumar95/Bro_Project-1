from django.urls import path
from category import views

urlpatterns = [
    path('',views.product_manager,name='productmanager'),
    path('product/add',views.product_add,name='productadd'),
    path('editproduct/<int:product_id>',views.product_edit,name='producteditor'),
    path('product/delete/<int:product_id>',views.delete_product,name='productdelete'),
    path('category',views.category_list,name='categorymanager'),
    path('category/add',views.category_list,name="addcategory"),
    path('category/edit/<int:category_id>',views.category_edit,name="editcategory"),
    path('category/delete/<int:category_id>',views.category_delete,name="delcategory"),
]
    