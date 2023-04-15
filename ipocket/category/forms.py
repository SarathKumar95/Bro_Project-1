from django.forms import CheckboxInput, DateInput, ModelForm,TextInput,NumberInput,Select,Textarea,FileInput
from django import forms
from category.models import *


class ProductTypeForm(ModelForm):
    
    class Meta:
        model = ProductType
        fields = '__all__'



class CategoryForm(ModelForm):

    class Meta:
        model = Categories
        fields = '__all__' 


class ProductForm(ModelForm):

    class Meta:
        model = Products
        fields = '__all__'
    

class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

        widgets= {
            'user': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'first_name': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'last_name': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'email': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'phone': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'address': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'state': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'city': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'pincode': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'total_price': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'tax_amount' : TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            'ship_amount': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            
            'coupon_amount': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            
            'payment_mode': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            
            'price_before_tax': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            'payment_id': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }
            ),
            
            'tracking_no': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }
            ),

            'message' : Textarea(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            
            'status' : Select(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
            
            
            'coupon': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
        }


        def clean(self):
            instance = getattr(self,'instance')

            print('Instance status is', instance.status)



class OrderItemForm(ModelForm):

    class Meta:
        model = OrderItem
        fields = '__all__' 

        widgets= {
            'order': Select(attrs={
                'class': "form-control  text-dark",
                'style' : "max-width: 300px",
            }),            
            'product': Select(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            'price': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            'quantity': TextInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            
             'item_status': Select(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),
        }


class CouponForm(ModelForm):
    
    class Meta:
        model = Coupon
        fields = '__all__'

        widgets= {
            'coupon_code': TextInput(attrs={
                'class': "form-control  text-dark",
                'style' : "max-width: 300px",
            }),            
            'valid_till': DateInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            'is_expired': CheckboxInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            'discount_percentage': NumberInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),            
            
             'minimum_amount': NumberInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            'maximum_amount': NumberInput(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 300px",
            }),

            'description': Textarea(attrs={
                'class': "form-control text-dark",
                'style' : "max-width: 600px",
            }),

        }

class BannerForm(ModelForm):
    
    class Meta:
        model = Banner
        fields = '__all__'

class ProductAttrForm(ModelForm):

    class Meta:
        model = ProductVariant
        fields = '__all__'
        exclude = ['product_id']


class AddColorForm(ModelForm):

    class Meta:
        model = Product_Color
        fields = '__all__'
        