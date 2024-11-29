from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from home.models import *
from home.forms import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import timedelta
from django.db.models import Sum, F
from django.db.models.functions import TruncDate, TruncMonth
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib import messages
from django.db.models import Q  # Import Q object
from reportlab.pdfgen import canvas


# Create your views here.
@login_required(login_url='login_admin')
def admin(request):
    add_product_form = AddProductForm()
    employee_form = EmployeeForm()
    user_form = UserAdminForm()
    customer_form = CustomerForm()
    cart_form = CartForm()
    cart_detail_form = CartDetailForm()
    category_form = CategoryForm()
    coupon_form = CouponsForm()
    import_product_form = ImportProductsForm()
    landing_page_form = LandingPagesForm()
    order_product_form = OrderProductForm()
    payment_form = PaymentForm()
    product_coupon_form = ProductCouponsForm()
    review_form = ReiewsForm()
    wishlist_form = WishlistsForm()
    
     #..cai gi nua
    
    all_product_coupon = ProductCoupons.objects.select_related('id_product', 'id_coupon').all()
    all_import_product_by_id = ImportProducts.objects.select_related('id_product').all()
    all_order_product_by_id = OrderProduct.objects.select_related('id_cart', 'id_coupon').all()
    all_cart_detail_by_id = CartDetail.objects.select_related('id_cart','id_product' ,'id_coupon').all()
    all_order_payment_by_id = Payment.objects.select_related('id_order').all()
    all_cart_by_id = Cart.objects.select_related('id_customer')
    all_customer_by_id = Customer.objects.select_related('id_user').all()
    unused_user_ids = Users.objects.filter(~Q(id_user__in=Customer.objects.values_list('id_user', flat=True)))
    
    if request.method == "POST":
        # Product
        if 'add_product' in request.POST:
            add_product_form = AddProductForm(request.POST, request.FILES) 
            if add_product_form.is_valid():
                add_product_form = add_product_form.save(commit=False)
                add_product_form.product_quantity = 0
                add_product_form.activate = False
                add_product_form.status = "Hết hàng"
                add_product_form.create_at = timezone.now()  # Thiết lập giá trị cho created_at
                add_product_form.update_at = timezone.now()
                add_product_form.create_by = request.user.username  # Thiết lập giá trị cho created_by
                add_product_form.update_by = request.user
                add_product_form.save()
                messages.success(request, 'Product added successfully!')
                return redirect(request.path) 
            else:
                print(add_product_form.errors)
                
        elif 'delete_product' in request.POST:
            id = request.POST.get('delete_product')
            product = Products.objects.get(id_product = id)
            product.delete()
            messages.success(request, 'Product deleted successfully!')
            return redirect(request.path) 
            
        elif 'edit_product' in request.POST:
            id = request.POST.get('edit_product')
            product = get_object_or_404(Products, id_product=id)
            form = AddProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product.status = "Hết hàng"
                product.activate = True
                product.update_at = timezone.now()
                product.update_by = request.user.username
                form.save()
                messages.success(request, 'Product edited successfully!')
                return redirect(request.path) 
            else:
                 print(form.errors)
                 
        
        
        elif 'add_customer' in request.POST:
            add_customer = CustomerForm(request.POST, request.FILES)
            user_id = request.POST.get('user_id')
            user = Users.objects.get(id_user = user_id)
            if add_customer.is_valid() and user:
                add_customer = add_customer.save(commit=False)
                add_customer.id_user = user
                add_customer.save()
                messages.success(request, f'Customer added successfully!')
                return redirect(request.path) 
            else:
                messages.warning(request, f'lỗi!{user}')
                
        elif 'delete_customer' in request.POST:
            id = request.POST.get('delete_customer')
            customer = Customer.objects.get(id_customer = id)
            if customer:
                customer.delete()
                messages.success(request, 'Customer deleted successfully!')   
            else:
                messages.warning(request, 'lỗi!')
            return redirect(request.path)      
        elif 'edit_customer' in request.POST:
            
            user_id = request.POST.get('user_id')
            customer_id = request.POST.get('customer_id')
            user = Users.objects.get(id_user = user_id)
            customer = get_object_or_404(Customer, id_customer = customer_id)
            form = CustomerForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form = form.save(commit=False)
                form.id_user = user
                form.save()
                messages.success(request, 'Customer edited successfully!')
            else:
                messages.warning(request, 'lỗi!')
            return redirect(request.path)
        
                 
        # Employee
        elif 'add_employee' in  request.POST:
            add_employee = EmployeeForm(request.POST, request.FILES)
            if add_employee.is_valid():
                add_employee.save()
                messages.success(request, 'Employee added successfully!')
            return redirect(request.path) 
        elif 'delete_employee' in request.POST:
            id = request.POST.get('delete_employee')
            employee = Employees.objects.get(id_emp = id)
            employee.delete()
            messages.success(request, 'Employee deleted successfully!')
            return redirect(request.path) 
        elif 'edit_employee' in request.POST:
            id = request.POST.get('edit_employee')
            employee = get_object_or_404(Employees, id_emp = id)
            form = EmployeeForm(request.POST, request.FILES, instance=employee)
            if form.is_valid():
                form.save()
                messages.success(request, 'Employee edited successfully!')
                return redirect(request.path)
            else:
                print(form.errors)

        # User
        elif 'add_user' in request.POST:
            add_user = UserAdminForm(request.POST, request.FILES)
            if add_user.is_valid():
                add_user = add_user.save(commit=False)
                add_user.create_at = timezone.now()  # Thiết lập giá trị cho created_at
                add_user.update_at = timezone.now()
                add_user.create_by = request.user.username  # Thiết lập giá trị cho created_by
                add_user.update_by = request.user.username
                add_user.save()
                messages.success(request, 'User added successfully!')
                return redirect(request.path)
            else:
                print(add_user.errors)
        elif 'delete_user' in request.POST:
            id = request.POST.get('delete_user')
            add_user = Users.objects.get(id_user = id)
            add_user.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect(request.path)
            
        elif 'edit_user' in request.POST:
            id = request.POST.get('edit_user')
            edit_user = get_object_or_404(Users, id_user = id)
            form = UserAdminForm(request.POST, request.FILES, instance=edit_user)
            
            if form.is_valid():
                
                edit_user.update_at = timezone.now()
                edit_user.update_by = request.user.username
                form.save()
                messages.success(request, 'User edited successfully!')
                return redirect(request.path)
            else:
                print(form.errors)
        
        
        # category
        elif 'add_category' in request.POST:
            add_category = CategoryForm(request.POST, request.FILES)
            if add_category.is_valid():
                add_category = add_category.save(commit=False)
                add_category.create_at = timezone.now()  # Thiết lập giá trị cho created_at
                add_category.update_at = timezone.now()
                add_category.create_by = request.user.username  # Thiết lập giá trị cho created_by
                add_category.update_by = request.user.username
                add_category.save()
                messages.success(request, 'Category added successfully!')
                return redirect(request.path)
            
        elif 'delete_category' in request.POST:
            id = request.POST.get('delete_category')
            delete_category = Categories.objects.get(id_category = id)
            delete_category.delete()
            messages.success(request, 'Category deleted successfully!')
            return redirect(request.path)
        
        elif 'edit_category' in request.POST:
            id = request.POST.get('edit_category')
            edit_category = get_object_or_404(Categories, id_category = id)
            form = CategoryForm(request.POST, request.FILES, instance=edit_category)
            if form.is_valid():
                edit_category.update_at = timezone.now()
                edit_category.update_by = request.user.username
                form.save()
                messages.success(request, 'Category edited successfully!')
                return redirect(request.path)
            else:
                print(form.errors)
        
        # coupon
        elif 'add_coupon' in request.POST:
            add_coupon = CouponsForm(request.POST, request.FILES)
            if add_coupon.is_valid():
                add_coupon = add_coupon.save(commit=False)
                # Chuyển đổi start_date thành đối tượng datetime
                time = (int)(add_coupon.time_used)
                # add_coupon.start_date = datetime.strptime(add_coupon.start_date, '%Y-%m-%d').date()  
                end_d = add_coupon.start_date + timedelta(days= time)
                # Tính toán end_date
                add_coupon.end_date = end_d
                add_coupon.activate = True
                add_coupon.create_at = timezone.now()  
                add_coupon.update_at = timezone.now()
                add_coupon.create_by = request.user.username  # Thiết lập giá trị cho created_by
                add_coupon.update_by = request.user.username
                add_coupon.save()
                messages.success(request, 'Coupon added successfully!')
                return redirect(request.path)
            
            
        elif 'delete_coupon' in request.POST:
            id = request.POST.get('delete_coupon')
            delete_coupon = Coupons.objects.get(id_coupon = id)
            delete_coupon.delete()
            messages.success(request, 'Coupon deleted successfully!')
            return redirect(request.path)
        
        
        elif 'edit_coupon' in request.POST:
            id = request.POST.get('edit_coupon')
            edit_coupon = get_object_or_404(Coupons, id_coupon = id)
            form = CouponsForm(request.POST, request.FILES, instance=edit_coupon)
            if form.is_valid():
                time = (int)(edit_coupon.time_used)
                # add_coupon.start_date = datetime.strptime(add_coupon.start_date, '%Y-%m-%d').date()  
                end_d = edit_coupon.start_date + timedelta(days= time)
                # Tính toán end_date
                edit_coupon.end_date = end_d
                edit_coupon.activate = True
                edit_coupon.update_at = timezone.now()
                edit_coupon.update_by = request.user.username
                edit_coupon.save()
                messages.success(request, 'Coupon edited successfully!')
                return redirect(request.path)
            else:
                print(form.errors)
        
        # product_coupon
        
        elif 'add_product_coupon' in request.POST:
            id_coupon = request.POST.get('coupon_id')
            name_product = request.POST.get('product_name')

            try:
                # Lấy đối tượng Coupon từ id_coupon
                coupon = Coupons.objects.get(pk=id_coupon) 
            except Coupons.DoesNotExist:
                messages.error(request, 'Coupon not found.')
                return redirect('dashboard')  

            product_ids = Products.objects.filter(product_name=name_product).values_list('id_product', flat=True)
            for product_id in product_ids:
                try:
                    product = Products.objects.get(pk=product_id)
                except Products.DoesNotExist:
                    continue  # Bỏ qua nếu không tìm thấy sản phẩm

                # Tạo form và gán giá trị từ POST request
                form = ProductCouponsForm(data={
                    'id_coupon': coupon.id_coupon,  # Gán ID của coupon
                    'id_product': product.id_product  # Gán ID của product
                })

                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)

            messages.success(request, 'Product Coupons added successfully!')
            return redirect('dashboard')  # Chuyển hướng về trang dashboard sau khi thêm 
        
        elif 'delete_product_coupon' in request.POST:
            id = request.POST.get('delete_product_coupon')
            delete_pc = ProductCoupons.objects.get (id = id)
            delete_pc.delete()
            messages.success(request, 'deleted successfully!')
            return redirect(request.path)

        elif 'edit_product_coupon' in request.POST:
            id_edit = request.POST.get('id_product_coupon')
            coupon_id_edit = request.POST.get('coupon_id')
            product_id_edit = request.POST.get('product_id')
            edit = get_object_or_404(ProductCoupons,id = id_edit)
            coupon = Coupons.objects.get(id_coupon = coupon_id_edit) 
            product = Products.objects.get(id_product = product_id_edit)
            form = ProductCouponsForm(data={
                    'id_coupon': coupon.id_coupon,  # Gán ID của coupon
                    'id_product': product.id_product  # Gán ID của product
                }, instance=edit)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        
        
        # import_product
                
        elif 'add_import_product' in request.POST:
            product_id = request.POST.get('product_id')
            import_quantity = request.POST.get('import_quantity')
            import_price = request.POST.get('import_price')
            supplier = request.POST.get('supplier')
            
            product = Products.objects.get(id_product= product_id) 
             
            product.product_quantity += (int)(import_quantity)  
             
            if product.product_quantity == 0 and product.status == 'Còn hàng':
                product.status = 'Hết hàng'
                product.activate = False
                        
            
            if product.product_quantity > 0:
                product.status = 'Còn hàng'
                product.activate = True
            product.save()
            add_import_product = ImportProductsForm(data={
                'id_product': product.id_product,
                'import_quantity': import_quantity,
                'import_price': import_price,
                'supplier': supplier
            })
            if add_import_product.is_valid():
                add_import_product = add_import_product.save(commit=False)
                add_import_product.create_at = timezone.now()  # Thiết lập giá trị cho created_at
                add_import_product.update_at = timezone.now()
                add_import_product.create_by = request.user.username  # Thiết lập giá trị cho created_by
                add_import_product.update_by = request.user.username
                add_import_product.save()
                messages.success(request, 'Added successfully!')
                return redirect(request.path)
            else:
                print(add_import_product.errors)
                
                
        elif 'delete_import_product' in request.POST:
            id = request.POST.get('delete_import_product')
            id_product = request.POST.get('id_pro')
            delete_imp_product = ImportProducts.objects.get(id_imp = id)
            update_quantity = Products.objects.get(id_product = id_product)
            if update_quantity.product_quantity >= delete_imp_product.import_quantity:
                update_quantity.product_quantity -= (int)(delete_imp_product.import_quantity)
            else:
               messages.warning(request, 'Sắp hết hàng!') 
            if update_quantity.product_quantity == 0:
                update_quantity.activate = False
                update_quantity.status = "Hết hàng"
            update_quantity.save()
            delete_imp_product.delete()
            messages.success(request, 'Deleted successfully!')
            return redirect(request.path)
        
        
        elif 'edit_import_product' in request.POST:
            id_product = (int)(request.POST.get('product_id'))
            id_imp = request.POST.get('id_imp')
            import_quantity = (int)(request.POST.get('import_quantity'))
            import_price = request.POST.get('import_price')
            supplier = request.POST.get('supplier')
            
            # xử lý logic quantity
            product_new = Products.objects.get(id_product = id_product)
            import_product = get_object_or_404(ImportProducts, id_imp =id_imp)
            product_old = Products.objects.get(id_product = import_product.id_product.id_product)
            print(product_old)
            print(import_product.id_product.id_product)
            if product_new.product_quantity >= 0:
                product_new.status = "Còn hàng" 
            else:
                product.status = "Hết hàng"
                product.activate = False   
            if import_product.id_product.id_product != id_product:
                if product_old.product_quantity < import_product.import_quantity:
                    messages.warning(request,"Lỗi logic: không hợp lệ")
                else:
                    product_old.product_quantity -= int(import_product.import_quantity)
                    product_new.product_quantity += int(import_product.import_quantity)

                
            else:
                if import_product.import_quantity != import_quantity:
                    if import_product.import_quantity > import_quantity:
                        a = product_new.product_quantity - int(import_product.import_quantity - import_quantity)
                        if a > 0:
                            product_new.product_quantity = a
                        elif a <= 0:
                            product_new.product_quantity = 0
                    elif import_product.import_quantity < import_quantity:
                        product_new.product_quantity += int(import_quantity - import_product.import_quantity) 
            
            
                
            product_old.save()
            product_new.save()
            
            form = ImportProductsForm(data={
                'id_product' : id_product,
                'import_quantity': import_quantity,
                'import_price': import_price,
                'supplier': supplier
            }, instance=import_product)
            if form.is_valid():
                form = form.save(commit=False)
                form.update_at = timezone.now()
                form.update_by = request.user.username
                form.save()
                messages.success(request, 'Edited successfully!')
                return redirect(request.path)
            else:
                print(form.errors)
        
        
        elif 'update_activate' in request.POST:
            print(request.POST.get)
            product_ids = [int(value) for key, value in request.POST.items() if key.startswith('product_id_')]
            print(product_ids)
            for product_id in product_ids:
                try:
                    product = Products.objects.get(pk=product_id)
                    activate_key = f'activate_{product_id}'
                    print(f"Processing product_id: {product_id}, activate_key in POST: {activate_key in request.POST}")
                    if activate_key in request.POST:
                        product.activate = True
                    else:
                        product.activate = False
                    product.save()
                except Products.DoesNotExist:
                    messages.warning(request, f"Sản phẩm không tồn tại: ID {product_id}")
            messages.success(request, 'Trạng thái kích hoạt đã được cập nhật!')
            return redirect(request.path)
        
        # order_product
        elif 'add_order_product' in request.POST:
            cart_id = request.POST.get('cart_id')
            coupon_id = request.POST.get('coupon_id')
            order_description = request.POST.get('order_description')
            total = request.POST.get('total')
            
            try:
                cart = Cart.objects.get(id_cart=cart_id)
                coupon = Coupons.objects.get(id_coupon=coupon_id)
            except (Cart.DoesNotExist, Coupons.DoesNotExist):
                messages.error(request, 'Cart or coupon not found.')
                return redirect(request.path)
            
            
            if cart.activate == False: 
                cart.activate = True
                
            total_new = cart.total_price - coupon.discount_value
            if total_new < 0:
                total_new = 0
            add_order_product = OrderProductForm(data={
                'id_cart': cart.id_cart,
                'id_coupon': coupon.id_coupon,
                'order_description': order_description,
                'total': total_new
            })
            if add_order_product.is_valid():
                order_product = add_order_product.save()
                
                add_payment = PaymentForm(data={
                    'id_order': order_product.id_order,
                    'payment_status': False,
                    'order_status': 'waiting for confirmation'
                })
                print(add_payment)
                if add_payment.is_valid():
                    
                    add_payment.save()
                    messages.success(request, 'Order and payment created successfully!')
                else:
                    # Xử lý lỗi của PaymentForm
                    print(add_payment.errors)
                
            else:
                print(add_order_product.errors)
            
            cart = cart.save()
            return redirect(request.path)   
        
        
        elif 'delete_order_product' in request.POST:
            id = request.POST.get('delete_order_product') 
            cart_id = request.POST.get('id_cart')
            delete_order = OrderProduct.objects.get(id_order = id)
            update_cart = Cart.objects.get(id_cart = cart_id)
            update_cart.activate = False
            update_cart.save()
            delete_order.delete()
            messages.success(request, "Deleted Sucessful!")
            return redirect(request.path)
        
        
        
        
        elif 'edit_order_product' in request.POST:
            # biến của order product
            order_id = request.POST.get('id_order')
            cart_id = request.POST.get('cart_id')
            coupon_id = request.POST.get('coupon_id')
            order_description = request.POST.get('order_description')
            payment_id = request.POST.get('id_payment')
            total = 0
            print (order_id + cart_id + coupon_id + order_description + "/n")
            # biến của Payment
            payment_status = request.POST.get('payment_status')
            order_status = request.POST.get('order_status')
            print(payment_status + order_status)
            
            coupon = get_object_or_404(Coupons, id_coupon = coupon_id)
            order = get_object_or_404(OrderProduct, id_order = order_id)
            payment = get_object_or_404(Payment, id_payment = payment_id)
            cart = get_object_or_404(Cart, id_cart = cart_id)
            old_cart = Cart.objects.get(id_cart = order.id_cart.id_cart)
            print(old_cart)
            
            
            if old_cart.id_cart != cart.id_cart:
                old_cart.activate = False
                cart.activate = True
            else:
                if order.id_coupon != coupon.id_coupon:
                    total = cart.total_price - coupon.discount_value
            if total <=0:
                total = 0
            
            print(total)  
            old_cart.save() 
            cart.save() 
            
            edit_order = OrderProductForm(data={
                'id_cart' : cart_id,
                'id_coupon': coupon_id,
                'order_description': order_description,
                'total': total
            },instance=order)
            
            edit_payment = PaymentForm(data={
                'id_order': order_id,
                'payment_status': payment_status,
                'order_status': order_status
            },instance=payment)
            
            if edit_order.is_valid():
                edit_order.save()
                messages.success(request, 'Edited Order successfully!')
            else:
                print(edit_order.errors)
            if edit_payment.is_valid():
                edit_payment.save()
                messages.success(request, 'Edited Payment successfully!')
            else:
                print(edit_payment.errors)
                
            return redirect(request.path)
        
        
        
        
        elif 'add_cart' in request.POST:
            customer_id = request.POST.get('customer_id')
            customer = Customer.objects.get(id_customer = customer_id)
            add_cart = CartForm(data={
                'id_customer': customer.id_customer
            })
            if add_cart.is_valid():
                add_cart = add_cart.save(commit=False)
                add_cart.total_price = 0
                add_cart.activate = False
                add_cart.create_at = timezone.now()
                add_cart.update_at = timezone.now()
                add_cart.save()
                messages.success(request, 'Added Cart successfully!')
                return redirect(request.path)
            else:
                print(add_cart.errors)
        
        elif 'delete_cart' in request.POST:
            id =request.POST.get('delete_cart')
            cart = get_object_or_404(Cart, id_cart = id)
            cart.delete()
            messages.success(request, 'Deleted Cart successfully!')
            return redirect(request.path)
        
        
        elif 'edit_cart' in request.POST:
            cart_id = request.POST.get('id_cart')
            customer_id = request.POST.get('customer_id')
            cart = Cart.objects.get(id_cart = cart_id)
            
            edit_cart = CartForm(data={
                'id_customer': customer_id
            }, instance=cart)
            if edit_cart.is_valid():
                edit_cart.update_at = timezone.now()
                edit_cart.save()
                messages.success(request, 'Edited Cart successfully!')
                return redirect(request.path)
            else:
                print(edit_cart.errors)
        
        
        elif 'add_cart_detail' in request.POST:
            cart_id = request.POST.get('cart_id')
            product_id = request.POST.get('product_id')
            coupon_id = request.POST.get('coupon_id')
            number = (int)(request.POST.get('number'))
            
            coupon = Coupons.objects.get(id_coupon = coupon_id)
            cart = Cart.objects.get(id_cart = cart_id)
            edit_product = Products.objects.get(id_product = product_id)
            
            if cart.activate == False:
            
                price = (number * edit_product.export_price) - coupon.discount_value
                if price <= 0:
                    price = 0
                cart.total_price += price
                edit_product.product_quantity -= number
                
                
                cart.save()
                edit_product.save()
                
                add_cart_detail = CartDetailForm(data={
                    'id_cart' : cart_id,
                    'id_product' : product_id,
                    'id_coupon' : coupon_id,
                    'number' : number 
                }) 
                
                if add_cart_detail.is_valid():
                    add_cart_detail = add_cart_detail.save(commit=False)
                    add_cart_detail.price = price
                    add_cart_detail.status_product = True
                    add_cart_detail.save()
                    messages.success(request, 'Added Cart Detail successfully!')
                
                else:
                    print(add_cart_detail.errors)
            else:
                messages.warning(request, "Giỏ hàng này đã được lên đơn hàng! không thể thực hiện thay đổi")
                
            return redirect(request.path)
            
        elif 'delete_cart_detail' in request.POST:
            id = request.POST.get('delete_cart_detail')
            delete_cart_detail = get_object_or_404(CartDetail, id = id)
            
            product = Products.objects.get(id_product = delete_cart_detail.id_product.id_product)
            cart = Cart.objects.get(id_cart = delete_cart_detail.id_cart.id_cart)
            
            if cart.activate == False:
                
                product.product_quantity += delete_cart_detail.number
                cart.total_price -= delete_cart_detail.price 
                
                product.save()
                cart.save()
                delete_cart_detail.delete()
                messages.success(request, 'returned product successfully!')
                messages.success(request, 'Updated cart successfully!')
                messages.success(request, 'Deleted Cart Detail successfully!')
                
            else:
                messages.warning(request, "Giỏ hàng này đã được lên đơn hàng! không thể thực hiện thay đổi")
            return redirect(request.path)
                
        elif 'edit_cart_detail' in request.POST:
            cart_id = request.POST.get('cart_id')
            product_id = request.POST.get('product_id')
            coupon_id = request.POST.get('coupon_id')
            number = (int)(request.POST.get('number'))     
            cart_detail_id = request.POST.get('id')
            
            cart_detail = get_object_or_404(CartDetail, id = cart_detail_id)
            product_old = get_object_or_404(Products, id_product = cart_detail.id_product.id_product)
            cart_old = get_object_or_404(Cart, id_cart = cart_detail.id_cart.id_cart)
            coupon = get_object_or_404(Coupons, id_coupon = coupon_id)
            product_new = get_object_or_404(Products, id_product =  product_id)
            cart_new = get_object_or_404(Cart, id_cart = cart_id)
            
            if cart_old.activate == False:
                
                if cart_new.activate == False:
            
                    price = (number * product_new.export_price) - coupon.discount_value
                    
                    if cart_detail.id_cart.id_cart != cart_new.id_cart:
                        cart_old.total_price -= cart_detail.price
                        cart_new.total_price += price
                    
                    if cart_detail.id_product.id_product != product_new.id_product:
                        product_old.product_quantity += cart_detail.number
                        product_new.product_quantity -= number
                    
                    product_old.save()
                    product_new.save()
                    cart_old.save()
                    cart_new.save()
                    
                    edit_cart_detail = CartDetailForm(data={
                        'id_cart' : cart_id,
                        'id_product' : product_id,
                        'id_coupon' : coupon_id,
                        'number' : number 
                    })
                    
                    if edit_cart_detail.is_valid():
                        edit_cart_detail = edit_cart_detail.save(commit=False)
                        edit_cart_detail.price =price
                        edit_cart_detail.status_product = True
                        edit_cart_detail.save()
                        messages.success(request, 'Edited Card Detail successfully!')
                    else:
                        print(edit_cart_detail.errors)
                
                else:
                    messages.warning(request, "Giỏ hàng bạn định chuyển đã được lên đơn hàng! không thể thực hiện thay đổi")
            
            else:
                messages.warning(request, "Giỏ hàng này đã được lên đơn hàng! không thể thực hiện thay đổi")
                
                
            return redirect(request.path)
        
        
        elif 'import_excel' in request.POST and request.FILES['excel_file']:
            excel_file = request.FILES['excel_file']
            
            # Kiểm tra định dạng tệp tin
            if not excel_file.name.endswith('.xlsx'):
                messages.error(request, 'File không đúng định dạng. Vui lòng chọn file .xlsx')
                return redirect('dashboard')

            # Đọc dữ liệu từ file Excel
            df = pd.read_excel(excel_file)
            
            # Thêm sản phẩm
            for index, row in df.iterrows():
                try:
                    # Lấy hoặc tạo danh mục sản phẩm
                    category_id =(int)( row['id_category'])
                    category = Categories.objects.get(id_category=category_id)  
                    # Tạo sản phẩm mới
                    Products.objects.create(
                        product_name=row['product_name'],
                        sku=row['sku'],
                        id_category=category,
                        export_price=(int)(row['export_price']),
                        product_quantity=row['product_quantity'],
                        product_description=row['product_description'],
                        image_product=row['image_product'],
                        brand=row['brand'],
                        size=row['size'],
                        color=row['color'],
                        activate=row.get('activate',True), # Trường hợp file excel không có cột activate thì mặc định là False
                        status=row.get('status',"Còn hàng"),
                        create_at = timezone.now(),
                        update_at = timezone.now(),
                        create_by= request.user.username ,
                        update_by= request.user.username
                        
                    )
                    messages.success(request, 'Import sản phẩm thành công!')
                except Categories.DoesNotExist:
                    # Xử lý trường hợp không tìm thấy danh mục (ví dụ: tạo mới hoặc bỏ qua)
                    messages.warning(request, f'Danh mục không tồn tại: ID {category_id}')
                    continue
                except Exception as e:
                    messages.error(request, f'Lỗi khi thêm sản phẩm {row["product_name"]}: {e}')
            
            return redirect(request.path)
        
        elif 'export_excel' in request.POST:
            # Lấy dữ liệu từ bảng Products
            filename = request.POST.get('filename', 'products.xlsx')
            products = Products.objects.all().values(
                'id_product', 'product_name', 'sku', 'id_category__id_category', 
                'export_price', 'product_quantity', 'product_description',
                'brand', 'size', 'color', 'activate', 'status',
                'create_at', 'update_at', 'create_by', 'update_by'
            )
            df = pd.DataFrame(products)
            df = df.rename(columns={'id_category__id_category': 'id_category'})

            # Chuyển đổi các cột datetime thành chuỗi có định dạng mong muốn
            df['create_at'] = df['create_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['update_at'] = df['update_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Tạo response để trả về file Excel
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Tạo writer và lưu DataFrame vào file Excel
            writer = pd.ExcelWriter(response, engine='openpyxl')
            df.to_excel(writer, index=False)  # index=False để không ghi cột index mặc định của DataFrame
            writer.close()

            return response
        
        
        
        elif 'export_bill' in request.POST:
            order_id = request.POST.get("order_id")
            # Lấy thông tin đơn hàng
            order = get_object_or_404(OrderProduct, id_order=order_id)
            payment = get_object_or_404(Payment, id_order=order_id)
            cart = order.id_cart
            cart_by = get_object_or_404(Cart, id_cart = cart.id_cart)
            cart_details = CartDetail.objects.filter(id_cart=cart.id_cart)
            status = payment.payment_status
            if status == True:
                payment_status = "Paid"
            else:
                payment_status = "Unpaid"
            # Tạo file PDF trong bộ nhớ
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'
            p = canvas.Canvas(response)
            
            # Tiêu đề hóa đơn
            p.setFont("Helvetica-Bold", 15)
            p.drawString(300, 800, "Bill")
            p.setFont("Helvetica", 12)
            p.drawString(100, 750, "-----------------------------------------------------------------------------------------------------")
            # Thông tin đơn hàng
            p.drawString(100, 720, f"ID ORDER: {order.id_order}")
            p.drawString(100, 700, f"ORDER DATE: {order.id_cart.update_at.strftime('%Y-%m-%d')}")  
            p.drawString(100, 680, "-----------------------------------------------------------------------------------------------------")
            # Thông tin khách hàng
            p.drawString(100, 640, f"CUSTOMER_NAME: {cart_by.id_customer.name_customer}")
            p.drawString(100, 620, f"ADDRESS: {cart_by.id_customer.address}")
            p.drawString(100, 600, f"PHONE: {cart_by.id_customer.phone}")
            # ... (Các thông tin khác của khách hàng)
            p.drawString(100, 560, "-----------------------------------------------------------------------------------------------------")
            # Thông tin thanh toán
            p.drawString(100, 520, f"PAYMENT STATUS: {payment_status}")  # Sử dụng get_..._display() để lấy label của choices
            p.drawString(100, 500, f"ORDER STATUS: {payment.order_status}")
            p.drawString(100, 460, "-----------------------------------------------------------------------------------------------------")
            # Chi tiết giỏ hàng
            y = 420
            for detail in cart_details:
                p.drawString(100, y, f"- {detail.id_product.product_name} x {detail.number}: {detail.price}")
                y -= 20
                
            p.drawString(100,y,f"COUPON: {order.id_coupon.code}")
            y -= 20
            p.drawString(100,y, "-----------------------------------------------------------------------------------------------------")
            y -= 20
            # Tổng tiền
            p.drawString(100, y, f"TOTAL: {order.total}")

            p.showPage()
            p.save()
            return response       
            
                        
    request.POST._mutable = True
    request.POST.clear()
    context = get_all()
    
    #...cai gi do
    context['user_form'] = user_form
    context['username'] = request.user.username
    context['add_product_form'] = add_product_form
    context['employee_form'] = employee_form
    context['customer_form'] = customer_form
    context['cart_form'] = cart_form
    context['cart_detail_form'] = cart_detail_form
    context['category_form'] = category_form
    context['coupon_form'] = coupon_form
    context['import_product_form'] = import_product_form
    context['landing_page_form'] = landing_page_form
    context['order_product_form'] = order_product_form
    context['payment_form'] = payment_form
    context['product_coupon_form'] = product_coupon_form
    context['review_form'] = review_form
    context['wishlist_form'] = wishlist_form
    
    context['all_product_coupon'] = all_product_coupon
    context['all_import_product_by_id'] = all_import_product_by_id
    context['all_order_product_by_id'] = all_order_product_by_id
    context['all_order_payment_by_id'] = all_order_payment_by_id
    context['all_cart_detail_by_id'] = all_cart_detail_by_id
    context['all_customer_by_id'] = all_customer_by_id
    context['all_cart_by_id'] = all_cart_by_id
    context['unused_user_ids'] = unused_user_ids
    # ... (trong view của bạn)
    daily_revenue = context['daily_revenue']
    monthly_revenue = context['monthly_revenue']
    
    daily_revenue_data = [
        {
            'x': data['date'].strftime('%Y-%m-%d'),  # Chuyển đổi thành chuỗi định dạng 'YYYY-MM-DD'
            'y': data['total_revenue']
        } for data in daily_revenue
    ]

    monthly_revenue_data = [
        {
            'x': data['month'].strftime('%Y-%m'),  # Chuyển đổi thành chuỗi định dạng 'YYYY-MM'
            'y': data['total_revenue']
        } for data in monthly_revenue
    ]
    context['daily_revenue'] = daily_revenue_data
    context['monthly_revenue'] = monthly_revenue_data
    print(daily_revenue)
    print(monthly_revenue)
    all_product_names = Products.objects.values_list('product_name', flat=True).distinct() 
    context['all_product_name'] = all_product_names
    
    # tổng doanh thu
    total_revenue_ee = OrderProduct.objects.aggregate(Sum('total'))['total__sum']
    inventory = Products.objects.aggregate(Sum('product_quantity'))['product_quantity__sum']
    total_order = OrderProduct.objects.count()
    #formatted_revenue = f"{total_revenue_ee:,}" 
    context['inventory'] = inventory
    print(inventory)
    context['total_order'] = total_order
    context['total_revenue_ee'] = total_revenue_ee
    
    return render(request, 'admin.html', context)


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.info(request, 'invalid')
            return redirect('login_admin')
    else:
        return render(request, 'login_admin.html')
        
def get_all():
    all_user = Users.objects.all()
    all_employee = Employees.objects.all()
    all_customer = Customer.objects.all()
    all_category = Categories.objects.all()
    all_product = Products.objects.all()
    all_import_product = ImportProducts.objects.all()
    all_coupon = Coupons.objects.all()
    all_productcoupon = ProductCoupons.objects.all()
    all_cart = Cart.objects.all()
    all_order_product = OrderProduct.objects.all()
    all_cart_detail = CartDetail.objects.all()
    all_payment = Payment.objects.all()
    all_review = Reviews.objects.all()
    all_wishlist= Wishlists.objects.all()
    all_landing_page = LandingPages.objects.all()
    
    daily_revenue = (
        OrderProduct.objects
        .annotate(date=TruncDate('id_cart__update_at'))  # Trích xuất ngày từ update_at của Cart
        .values('date')
        .annotate(total_revenue=Sum('total'))
        .order_by('date')
    )
    
    monthly_revenue = (
        OrderProduct.objects
        .annotate(month=TruncMonth('id_cart__update_at'))  # Trích xuất tháng từ update_at của Cart
        .values('month')
        .annotate(total_revenue=Sum('total'))
        .order_by('month')
    )
    context = {
        'all_user': all_user,
        'all_employee': all_employee,
        'all_customer': all_customer,
        'all_category': all_category,
        'all_product': all_product,
        'all_import_product': all_import_product,
        'all_coupon': all_coupon,
        'all_productcoupon': all_productcoupon,
        'all_cart': all_cart,
        'all_order_product': all_order_product,
        'all_cart_detail': all_cart_detail,
        'all_payment': all_payment,
        'all_review': all_review,
        'all_wishlist': all_wishlist,
        'all_landing_page': all_landing_page,
        'daily_revenue': daily_revenue,
        'monthly_revenue': monthly_revenue
    }   
    return context
    









# def import_products(request):
#     if request.method == 'POST' and request.FILES['excel_file']:
#         excel_file = request.FILES['excel_file']
        
#         # Kiểm tra định dạng tệp tin
#         if not excel_file.name.endswith('.xlsx'):
#             messages.error(request, 'File không đúng định dạng. Vui lòng chọn file .xlsx')
#             return redirect('dashboard')

#         # Đọc dữ liệu từ file Excel
#         df = pd.read_excel(excel_file)
        
#         # Thêm sản phẩm
#         for index, row in df.iterrows():
#             try:
#                 # Lấy hoặc tạo danh mục sản phẩm
#                 category, _ = Categories.objects.get_or_create(category_name=row['id_category'])
#                 # Tạo sản phẩm mới
#                 Products.objects.create(
#                     product_name=row['product_name'],
#                     sku=row['sku'],
#                     id_category=category,
#                     export_price=row['export_price'],
#                     product_quantity=row['product_quantity'],
#                     product_description=row['product_description'],
#                     image_product=row['image_product'],
#                     brand=row['brand'],
#                     size=row['size'],
#                     color=row['color'],
#                     activate=row.get('activate',False), # Trường hợp file excel không có cột activate thì mặc định là False
#                     status=row.get('status',"Hết hàng"),
#                     created_by=request.user.username if request.user.is_authenticated else 'anonymous',
#                     updated_by=request.user.username if request.user.is_authenticated else 'anonymous'
#                 )
#             except Exception as e:
#                 messages.error(request, f'Lỗi khi thêm sản phẩm {row["product_name"]}: {e}')
#         messages.success(request, 'Import sản phẩm thành công!')
        
#     return redirect('dashboard')  # Chuyển hướng về trang dashboard sau khi import
