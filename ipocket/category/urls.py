from django.urls import path
from category import views

urlpatterns = [
    path('',views.product_manager,name='productmanager'),
    path('product/add',views.product_add,name='productadd'),
    path('editproduct/<int:product_id>',views.product_edit,name='producteditor'),
    path('product/delete/<int:product_id>',views.delete_product,name='productdelete'),
    path('producttype/list',views.producttype_list,name='product-type-list'),
    path('producttype/add',views.producttype_list,name='product-type-add'),
    path('producttype/edit/<int:sub_cat_id>',views.producttype_edit,name='product-type-edit'),
    path('producttype/delete/<int:sub_cat_id>',views.producttype_delete,name='product-type-delete'),
    path('category/list',views.list_categories,name='category-list'),
    path('category/add', views.list_categories,name='category-add'),
    path('category/edit/<int:category_id>', views.edit_categories,name='category-edit'),
    path('category/delete/<int:category_id>', views.delete_categories,name='category-delete')
    
]
    