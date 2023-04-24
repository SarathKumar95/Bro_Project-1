from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.home_page, name='home'),
    path('register', views.register, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('myaccount',views.myaccount, name='userhome'),
    path('myorder',views.myorder, name='my-order'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('usermanager',views.user_manager, name='usermanager'),
    path('blockuser/<int:id>',views.block_user,name='blockuser'),
    path('unblockuser/<int:id>', views.unblock_user, name='unblockuser'),
    path('products/',views.products,name="productspage"),
    path('products/type/<int:cat_id>/<int:subcat_id>',views.product_filter,name="type"),
    path('products/filter/type/<int:typeid>',views.product_type_filter,name="product-type-filter"),
    path('products/sortbyprice/ascending',views.sortbyprice_ascending,name="product-sortybyprice-ascending"),
    path('products/sortbyprice/descending',views.sortbyprice_descending,name="product-sortybyprice-descending"),
    path('products/sortbynew',views.sortbynew,name="product-sortybynew"),
    path('item/<int:product_id>',views.item,name="itempage"),
    path('item/cart/add',views.cart_add,name="cart-add"),
    path('item/cart/list',views.cart_list,name="cart-list"),
    path('item/cart/list/delete',views.cart_delete,name="cart-delete"),
    path('item/cart/list/update',views.cart_update,name="cart-update"),
    path('checkout',views.checkout,name='checkout'),
    #path('complete',views.payment_complete,name='complete'),
    #path('order/<str:t_no>',views.orderPage,name='order-placed'),
    path('ordermanager',views.order_manager, name='order-list'),
    path('ordermanager/edit/<int:id>',views.order_edit, name='order-edit'),
    path('ordermanager/info/<int:id>',views.order_info, name='order-info'),
    path('ordermanager/delete/<int:id>',views.order_delete, name='order-delete'),
    path('orderitem/edit/<int:id>',views.orderitem_edit, name='orderitem-edit'),
    path('orderitem/info/delete/<int:id>',views.orderitem_delete, name='orderitem-delete'),
    path('orderitem/info/cancel/<int:id>',views.orderitem_cancel, name='orderitem-cancel'),
    path('orderpage/<str:tracking_no>',views.OrderPage, name='order-page'),
    #path('guest',views.guest,name='guest')     
    path('ordereditem/<int:id>',views.ordered, name='ordered-items'),
    path('razorpay',views.razor_checkout, name='razorpay'),
    path('search', views.search_product, name='search-product'),
    path('invoice/<str:tracking_no>', views.viewInvoice, name='view-invoice'),
    path('signinOTP',views.signinOTP, name='signinOTP'),
    path('VerifyOTP/+<int:phone>',views.verifyOTP, name='otp-verify'),
    path('coupon/all',views.coupon_all, name='coupon-all'),
    path('coupon/post',views.coupon_post, name='coupon-post'),
    path('coupon/delete',views.coupon_delete, name='coupon-delete'),
    path('manager/coupon',views.coupon_manager, name='coupon-manager'),
    path('manager/coupon/add',views.coupon_add, name='coupon-add'),
    path('manager/coupon/edit/<int:coupon_id>',views.coupon_editor, name='coupon-editor'),
    path('manager/coupon/delete/<int:coupon_id>',views.coupon_delete_admin, name='coupon-deleteAdmin'),
    path('personal',views.personal,name='personal'),
    path('manageaddresses',views.manage_address,name='manage-address'),
    path('myorders/return/<int:itemID>',views.returnOrder,name='return-order'),
    path('chart', views.chart,name='chart'),
    path('salesreport',views.sales_report,name='sales-report'),
    path('salescsv',views.sales_csv,name='sales-csv'),
    path('getprice',views.get_product,name='get-product'),                
    path('checkprice',views.check_price,name='check-price'),
    path('productprices',views.product_prices,name='product-prices'),
    path('landingmanager',views.landing_page,name='landing'),
    path('productmanager/productattribute/list/<int:id>',views.list_productattr,name='product-attrList'),                                
    path('productmanager/productattribute/add',views.add_productattr,name='product-attrAdd'), 
    path('productmanager/productattribute/delete/<int:id>',views.delete_productattr,name='product-attrDel'),                                
    path('productmanager/productattribute/edit/<int:id>/<int:proID>',views.edit_productattr,name='product-attrEdit'),                                
    path('banner/delete',views.delete_banner,name='delete-Banner'),
    path('banner/edit/<int:id>',views.edit_Banner,name='edit-Banner'),
    path('select/feat',views.select_feat,name='selectFeat'),
    # path('productmanager/addColor',views.add_color,name='add-Color'), 
    path('productmanager/listColors/<int:id>',views.list_colors,name='list-Colors'),
    path('productmanager/listColors/delete/<int:id>',views.delete_color,name='delete-color'),
    path('productmanager/listColors/edit/<int:id>',views.edit_color,name='edit-color'),
    path('getColorprice',views.get_product_colorPrice,name='get-product-colorPrice'),

    path('productmanager/productstock/list/',views.list_productstock,name='product-stockList'),                                
    path('productmanager/productstock/delete/<int:variant_id>',views.delete_productStock,name='product-StockDel'),                                
    path('productmanager/productstock/edit/<int:variant_id>',views.edit_productstock,name='product-StockEdit'),                                

            
]
