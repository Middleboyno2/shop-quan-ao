from django import forms
from home.models import Products
from .models import *



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'sku', 'id_category', 'export_price', 'image_product', 'brand', 'size', 'color', 'product_description']
        widgets = {
            'product_quantity' : forms.HiddenInput(),
            'activate'  : forms.HiddenInput(),
            'status' : forms.HiddenInput(),
            'create_at': forms.HiddenInput(),
            'update_at': forms.HiddenInput(),
            'create_by': forms.HiddenInput(),
            'update_by': forms.HiddenInput(),
            
        }




class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['emp_name', 'email', 'phone', 'address', 'salary']  # Liệt kê các trường bạn muốn đưa vào form
        widgets = {
           
        }
        
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['avatar','account_type','password']
        widgets = {
            'create_at': forms.HiddenInput(),
            'update_at': forms.HiddenInput(),
            'create_by': forms.HiddenInput(),
            'update_by': forms.HiddenInput(),
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model =Customer
        fields = ['id_user', 'name_customer', 'email', 'phone', 'address']
        widgets = {
            'id_user': forms.HiddenInput(),
        }

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['id_customer' ]
        widgets = {
            'total_price' : forms.HiddenInput(),
            'activate' : forms.HiddenInput(),
            'create_at': forms.HiddenInput(),
            'update_at': forms.HiddenInput(),
        }
    
class CartDetailForm(forms.ModelForm):
    class Meta:
        model = CartDetail
        fields = ['id_cart', 'id_product', 'id_coupon', 'number']
        widgets = {
            'price': forms.HiddenInput(),
            'status_product': forms.HiddenInput() 
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['category_name', 'icon', 'image_banner']
        widgets = {
            'create_at': forms.HiddenInput(),
            'update_at': forms.HiddenInput(),
            'create_by': forms.HiddenInput(),
            'update_by': forms.HiddenInput(),
        }
        
class CouponsForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = ['code', 'discount_value', 'discount_type', 'time_used', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.HiddenInput(),
            'activate': forms.HiddenInput(),
            'create_at': forms.HiddenInput(),
            'update_at': forms.HiddenInput(),
            'create_by': forms.HiddenInput(),
            'update_by': forms.HiddenInput(),
        }

class ImportProductsForm(forms.ModelForm):
    class Meta:
        model = ImportProducts
        fields = ['id_product', 'import_quantity', 'import_price', 'supplier']
        widgets = {
            'create_at': forms.HiddenInput(),
            'update_at': forms.HiddenInput(),
            'create_by': forms.HiddenInput(),
            'update_by': forms.HiddenInput(),
        }
    
class LandingPagesForm(forms.ModelForm):
    class Meta:
        model = LandingPages
        fields = ['id_emp', 'image']
        widgets = {
            'activate' : forms.HiddenInput(),
            'create_at': forms.HiddenInput(),
            'update_at': forms.HiddenInput(),
            'create_by': forms.HiddenInput(),
            'update_by': forms.HiddenInput(),
        }
    
class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['id_cart', 'id_coupon', 'order_description', 'total']
        
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['id_order', 'payment_status', 'order_status']
        
class ProductCouponsForm(forms.ModelForm):
    class Meta:
        model = ProductCoupons
        fields = ['id_coupon', 'id_product']
        
class ReiewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['id_customer', 'star', 'review_description']
        
class WishlistsForm(forms.ModelForm):
    class Meta:
        model = Wishlists
        fields = ['id_customer', 'id_product']