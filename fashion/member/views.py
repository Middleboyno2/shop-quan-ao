from django.shortcuts import *
from django.http import HttpResponse
from home.models import *
import json
from django.contrib.auth.forms import UserCreationForm
from member.form import *
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import qrcode
from io import BytesIO


def Home(request):
    img = LandingPages.objects.order_by('?').first()
    if not img:
        img = None 
    featured_products = Products.objects.order_by('-product_quantity')[:8]
    latest_products = Products.objects.order_by('-create_at')[:4]
    categories = Categories.objects.all()
    context = {
        'img': img,
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    }
    return render(request, 'index.html', context)



def Product(request, id_product):
    product = Products.objects.get(id=id_product)
    categories = Categories.objects.all()
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'shop-details.html', context)

def add_to_cart(request):
    product_id = request.GET.get('product_id')
    if product_id:
        product = get_object_or_404(Products, id_product=product_id) 
        coupons = Coupons.objects.filter( discount_type = 'discount_product')
        return render(request, 'shop-details.html', {'product': product, 'coupons': coupons})
    return redirect('home')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            customer = Customer.objects.get(id_user_id=user_id)
            orders = OrderProduct.objects.filter(id_cart__id_customer=customer)
            payments = Payment.objects.filter(id_order__in=orders)

            context = {
                'orders': orders,
                'payments': payments
            }

            return render(request, 'checkout.html', context)
        
        except Customer.DoesNotExist:
            messages.error(request, 'Không tìm thấy thông tin khách hàng.')
            return redirect('login')

    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')

def process_payment_view(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')  
        payment = get_object_or_404(Payment, pk=payment_id)
        payment.payment_status = 1  
        payment.order_status = 'confirmed'    
        payment.save()
        return redirect('/order-payment/') 
    return render(request, 'checkout.html')

def delete_order_view(request, order_id):
    order = get_object_or_404(OrderProduct, id_order=order_id)
    order.delete()
    return redirect('checkout')

def shopping_cart(request):
    id_user = request.session.get('user_id')
    
    if id_user:
        try:
            customer = Customer.objects.get(id_user=id_user)
            cart = Cart.objects.filter(id_customer=customer, activate=False).first()
            if not cart:
                cart = Cart.objects.create(id_customer=customer, activate=False, total_price = 0, create_at = timezone.now(), update_at = timezone.now() )
            cart_details = CartDetail.objects.filter(id_cart=cart.id_cart)
            
            total_price = 0
            for detail in cart_details:
                # detail.product_total = detail.id_product.export_price * detail.number
                total_price = detail.price
                detail.product_image = detail.id_product.image_product

            context = {
                'customer': customer,
                'cart': cart,
                'cart_details': cart_details,
                'total_price': total_price,
            }

            if request.method == 'POST':
                product_id = request.POST.get('product_id')
                quantity = int(request.POST.get('quantity', 1)) 
                existing_detail = cart_details.filter(id_product=product_id).first()
                
                if existing_detail:
                    existing_detail.number += quantity
                    existing_detail.save()
                    messages.success(request, 'Đã cập nhật số lượng sản phẩm trong giỏ hàng.')
                else:
                    product = Products.objects.get(pk=product_id)
                    price = (int)(product.export_price * quantity)
                    new_detail = CartDetail.objects.create(
                        id_cart=cart,
                        id_product=product,
                        number=quantity,
                        price=price,
                        status_product=1  
                    )
                    messages.success(request, 'Đã thêm sản phẩm vào giỏ hàng.')

                return redirect('shopping_cart')

            return render(request, 'shopping-cart.html', context)

        except Customer.DoesNotExist:
            messages.error(request, 'Không tìm thấy thông tin khách hàng.')
            return redirect('login')
        
        except Cart.DoesNotExist:
            messages.info(request, 'Không tìm thấy giỏ hàng cho khách hàng này.')
            return render(request, 'shopping-cart.html', {})
    
    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = Users.objects.get(token=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id_user
                    request.session['user_avatar'] = user.avatar.url
                    try:
                        customer = Customer.objects.get(id_user=user.id_user)
                        request.session['customer_name'] = customer.name_customer
                        request.session['customer_email'] = customer.email
                    except Customer.DoesNotExist:
                        pass
                    return redirect('/')
                else:
                    user = None
            except Users.DoesNotExist:
                user = None

            if user is None:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            avatar_link = "images/image_user/image_user.png"
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

      
            if len(password) < 8:
                messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự.')
                return render(request, 'register.html', {'form': form})

      
            if Users.objects.filter(token=username).exists():
                messages.error(request, 'Tên đăng nhập đã tồn tại.')
                return render(request, 'register.html', {'form': form})

       
            if Customer.objects.filter(email=email).exists():
                messages.error(request, 'Email đã tồn tại.')
                return render(request, 'register.html', {'form': form})

            hashed_password = make_password(password)
            user = Users.objects.create(
                avatar=avatar_link,
                account_type='customer',
                token=username,
                password=hashed_password,
                create_at=timezone.now(),
                update_at=timezone.now(),
                create_by='admin',
                update_by='admin'
            )

      
            customer = Customer.objects.create(
                id_user=user,
                name_customer=name,
                email=email,
                phone=phone,
                address=address
            )

     
            Cart.objects.create(
                id_customer=customer,
                total_price=0,
                activate=0,
                create_at=timezone.now(),
                update_at=timezone.now()
            )

          
            messages.success(request, 'Đăng ký thành công. Bạn có thể đăng nhập ngay bây giờ.')
            return redirect('login')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin đăng ký.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def some_view(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = Users.objects.get(id_user=user_id)
            user_name = user.username
            
        except Users.DoesNotExist:
            pass
        if 'customer_name' in request.session:
            customer_name = request.session['customer_name']
            context = {'user_name': user_name, 'customer_name': customer_name}
        else:
            context = {'user_name': user_name}    
        return render(request, 'some_template.html', context)
    else:
        return redirect('/login/')
    

def profile(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id_user=user_id)
        customer = Customer.objects.get(id_user=user_id)

        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.password = new_password
                user.save()
                messages.success(request, 'Đổi mật khẩu thành công.')
                return redirect('profile')
            else:
                messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
        else:
            form = ChangePasswordForm()

        context = {
            'user': user,
            'customer': customer,
            'form': form
        }
        return render(request, 'profile.html', context)
    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')
    
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'customer_name' in request.session:
        del request.session['customer_name']
    return redirect('/')

def change_password(request):
    user_id = request.session.get('user_id')  
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        try:
            user = Users.objects.get(id_user=user_id)
            user.password = new_password   
            user.save()
            messages.success(request, 'Đổi mật khẩu thành công.')
            return redirect('profile')
        except Users.DoesNotExist:
            messages.error(request, 'Không tìm thấy người dùng.')
            return redirect('profile')   
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
            return redirect('profile')  
    return render(request, 'profile.html')

def shop(request):
    categories = Categories.objects.all()
    brands = Products.objects.values_list('brand', flat=True).distinct()
    category_id = request.GET.get('category_id')
    sort_by_price = request.GET.get('sort_by_price')
    search_query = request.GET.get('search_query')
    products = Products.objects.all()
    if category_id:
        try:
            category_id = int(category_id)   
            products = products.filter(id_category=category_id)
        except ValueError:
            pass  
    if search_query:
        products = products.filter(product_name__icontains=search_query)
    if sort_by_price == 'low_to_high':
        products = products.order_by('export_price')
    elif sort_by_price == 'high_to_low':
        products = products.order_by('-export_price')
    context = {
        'categories': categories,
        'brands': brands,
        'products': products,
        'sort_by_price': sort_by_price,
    }
    return render(request, 'shop.html', context)

def wishlist(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            customer = Customer.objects.get(id_user_id=user_id)
            wishlists = Wishlists.objects.filter(id_customer=customer)
            wishlist_products = []
            for wishlist in wishlists:
                product = wishlist.id_product
                wishlist_products.append({
                    'product_name': product.product_name,
                    'image_product': product.image_product,
                    'export_price': product.export_price,
                    'id_product': product.id_product  
                })
            context = {
                'wishlist_products': wishlist_products,
            }
            return render(request, 'wishlist.html', context)
        except Customer.DoesNotExist:
            messages.error(request, 'Không tìm thấy thông tin khách hàng.')
            return redirect('login') 
    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')  

def delete_wishlist_item(request):
    if request.method == 'DELETE':
        product_id = request.GET.get('product_id')
        
        try:
            wishlist_item = Wishlists.objects.get(id_product_id=product_id)
            wishlist_item.delete()
            
            return JsonResponse({'message': 'Item deleted successfully.'}, status=200)
        
        except Wishlists.DoesNotExist:
            return JsonResponse({'message': 'Item does not exist.'}, status=404)
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Products, id_product=product_id)
    user_id = request.session.get('user_id')

    if user_id:
        try:
            customer = Customer.objects.get(id_user_id=user_id)
            if Wishlists.objects.filter(id_customer=customer, id_product=product).exists():
                messages.info(request, 'Sản phẩm đã có trong danh sách yêu thích của bạn.')
            else:
                wishlist, created = Wishlists.objects.get_or_create(id_customer=customer, id_product=product)
                if created:
                    messages.success(request, 'Đã thêm sản phẩm vào danh sách yêu thích.')
                else:
                    messages.info(request, 'Sản phẩm đã có trong danh sách yêu thích của bạn.')
            return redirect('product_detail', id_product=product_id)
        except Customer.DoesNotExist:
            messages.error(request, 'Không tìm thấy thông tin khách hàng.')
            return redirect('login')
    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')
        


def product_detail(request, id_product):
    product = get_object_or_404(Products, id_product=id_product)
    context = {
        'product': product
    }
    return render(request, 'shop-details.html', context)

def add_to_cart2(request, product_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            try:
                customer = Customer.objects.get(id_user=user_id)
                cart = Cart.objects.filter(id_customer=customer, activate=False).first()
                if not cart:
                    cart = Cart.objects.create(id_customer=customer, activate=False, total_price = 0, create_at = timezone.now(), update_at = timezone.now() )
                    
                product = get_object_or_404(Products, id_product=product_id)
                quantity = int(request.POST.get('quantity', 1))
                coupon_id = request.POST.get('coupon', None)
                if product.product_quantity > quantity:
                    product.product_quantity -= quantity
                elif product.product_quantity == 0:
                    product.status = "Hết hàng"
                    product.save()
                    messages.warning(request, 'Sản phẩm hết hàng')
                    return redirect('shop_details', product_id=product_id)
                else:
                    messages.warning(request, f'Sản phẩm còn {product.product_quantity}, vui lòng nhập lại số lượng sản phẩm' )
                    return redirect('shop_details', product_id=product_id)
                product.save()
                if coupon_id:
                    try:
                        product_coupon = Coupons.objects.filter(id_coupon=coupon_id, discount_type = 'discount_product').first()
                        if product_coupon:
                            price = (int )(product.export_price * quantity) - product_coupon.discount_value
                        else:
                            price = (int )(product.export_price * quantity)
                    except Coupons.DoesNotExist:
                        messages.error(request, 'Mã coupon không hợp lệ.')
                        return redirect('shop_details', product_id=product_id)
                else:
                    product_coupon = None 
                    
                
                cart.total_price += price
                cart.save()
                
                cart_detail, created = CartDetail.objects.get_or_create(
                    id_cart=cart,
                    id_product=product,
                    defaults={
                        'id_coupon': product_coupon,
                        'number': quantity,
                        'price': price,
                        'status_product': True
                    }
                )

                if not created:
                    cart_detail.number += quantity
                    cart_detail.save()

                messages.success(request, 'Đã thêm sản phẩm vào giỏ hàng.')
            
            except Customer.DoesNotExist:
                messages.error(request, 'Không tìm thấy thông tin khách hàng.')
                return redirect('login')
            
            except Products.DoesNotExist:
                messages.error(request, 'Sản phẩm không tồn tại.')
            
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        
        else:
            messages.error(request, 'Bạn chưa đăng nhập.')
            return redirect('login')

    return redirect('shoping-cart')

def delete_cart_item_view(request):
    try:
        cart_detail_id = request.POST.get('cart_detail_id')
        cart_detail = CartDetail.objects.get(id=cart_detail_id)
        cart_detail.delete()
        return HttpResponse(json.dumps({'deleted': True}), content_type="application/json")
    except CartDetail.DoesNotExist:
        return HttpResponse(json.dumps({'deleted': False}), content_type="application/json")



def order_and_payment_view(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            customer = Customer.objects.get(id_user_id=user_id)
            orders = OrderProduct.objects.filter(id_cart__id_customer=customer)
            payments = Payment.objects.filter(id_order__in=orders)
           
            # for order in orders:
            #     order_payment_status = []
            #     for payment in payments:
            #         if payment.id_order == order:
            #             order_payment_status.append(payment.payment_status)
            #     order.payment_status = order_payment_status

            context = {
                'orders': orders,
                'payments': payments,
                
            }

            return render(request, 'checkout.html', context)
        except Customer.DoesNotExist:
            messages.error(request, 'Không tìm thấy thông tin khách hàng.')
            return redirect('login')
    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')
    

def order_and_payment(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            customer = Customer.objects.get(id_user_id=user_id)
            cart = Cart.objects.filter(id_customer=customer, activate=False).first()
            if cart == "":
                return redirect('shoping-cart')
            cart_details = CartDetail.objects.filter(id_cart=cart)
            total_price = sum(detail.price for detail in cart_details)

            if request.method == 'POST':
                coupon_code = request.POST.get('coupon_code')
                try:
                    coupon = Coupons.objects.get(code=coupon_code)
                    total_price = total_price - coupon.discount_value
                except Coupons.DoesNotExist:
                    coupon = None
                    messages.error(request, 'Mã coupon không hợp lệ.')
                    return redirect('shoping-cart')
                
                product_details = CartDetail.objects.filter(id_cart=cart).values_list('id_product', 'number')
                product_ids = [detail[0] for detail in product_details]
                product_quantities = {detail[0]: detail[1] for detail in product_details}
                products = Products.objects.filter(id_product__in=product_ids)
                order_description = ", ".join(f"{product.product_name} x {product_quantities[product.id_product]}" for product in products)
                order = OrderProduct.objects.create(
                    id_cart=cart,
                    id_coupon=coupon,
                    order_description=order_description,
                    total=total_price
                )
                Payment.objects.create(
                    id_order=order,
                    payment_status= False,  
                    order_status="waiting for confirmation"  
                )
                cart.activate = True
                cart.save()
                messages.success(request, 'Đặt hàng thành công!')
                return redirect('order_payment')
            else:
                return render(request, 'shopping-cart.html', {
                    'cart_details': cart_details,
                    'total_price': total_price
                })
        except Customer.DoesNotExist:
            messages.error(request, 'Không tìm thấy thông tin khách hàng.')
            return redirect('login')
        except Cart.DoesNotExist:
            messages.error(request, 'Giỏ hàng của bạn trống.')
            return redirect('checkout')
    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')
    

def all_reviews(request):
    user = request.session.get('user_id')
    user = Users.objects.get(id_user=user)
    reviews = Reviews.objects.select_related('id_customer').all()
    return render(request, 'reviews.html', {'reviews': reviews, 'user': user})

def post_review(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id') 
        customer = Customer.objects.get(id_user_id=user_id) 
        star = request.POST.get('star')
        review_description = request.POST.get('review_description')
        Reviews.objects.create(id_customer=customer, star=star, review_description=review_description)
        return redirect('all_reviews')
    return redirect('all_reviews') 




def confirm_delivery_view(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')  
        payment = get_object_or_404(Payment, pk=payment_id) 
        payment.order_status = 'delivered successfully'
        payment.save()
        return redirect('/order-payment/') 
    return render(request, 'checkout.html')

def generate_qr_code(request):
    phone_number = '09090090'
  
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = f"momo://transfer?receiver={phone_number}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')

def process_payment_momo(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')  
        payment = get_object_or_404(Payment, pk=payment_id)
        order = payment.id_order   

        return render(request, 'checkoutMOMO.html', {
            'payment': payment,
            'order': order,
        })

    return render(request, 'checkoutMOMO.html')