from django import forms
from django.contrib import messages
from home.models import Coupons
from django.shortcuts import redirect

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label='Mật khẩu mới')


class RegistrationForm(forms.Form):
    name = forms.CharField(label="Họ và tên", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    address = forms.CharField(label="Địa chỉ", max_length=100)
    phone = forms.CharField(label="Điện thoại", max_length=15)
    username = forms.CharField(label="Tên Đăng Nhập", max_length=100)
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)
    username = forms.CharField(label="Tên Đăng Nhập", max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    


class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    card_number = forms.CharField(max_length=16, required=False)
    expiry_date = forms.CharField(max_length=5, required=False)
    cvv = forms.CharField(max_length=3, required=False)
    coupon_id = forms.IntegerField(required=False)
    coupon_id = forms.IntegerField(required=False, label='Coupon ID')



def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupons.objects.get(code=coupon_code)
            # Apply coupon logic here
            messages.success(request, 'Mã giảm giá đã được áp dụng thành công.')
        except Coupons.DoesNotExist:
            messages.error(request, 'Mã giảm giá không hợp lệ.')
    return redirect('checkout')