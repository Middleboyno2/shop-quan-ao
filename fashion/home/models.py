

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models




class Cart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey('Customer', models.DO_NOTHING, db_column='id_customer')
    total_price = models.IntegerField()
    activate = models.BooleanField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cart'


class CartDetail(models.Model):
    id = models.AutoField(primary_key=True)
    id_cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='id_cart')
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')
    id_coupon = models.ForeignKey('Coupons', models.DO_NOTHING, db_column='id_coupon', blank=True, null=True)
    number = models.IntegerField()
    price = models.IntegerField()
    status_product = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cart_detail'


class Categories(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="images/image_categories/")  # Sử dụng ImageField cho hình ảnh
    image_banner = models.ImageField(upload_to="images/banner/")
    create_at = models.DateTimeField(auto_now_add=True)  
    update_at = models.DateTimeField(auto_now=True)      
    create_by = models.CharField(max_length=50)
    update_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categories'


class Coupons(models.Model):
    type = {
        'discount': 'Discount', 
        'discount_product': 'Discount Product'
    }
    id_coupon = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    discount_value = models.IntegerField()
    discount_type = models.CharField(
        max_length=20, 
        choices=type
    ) 
    time_used = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    activate = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    create_by = models.CharField(max_length=50)
    update_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'coupons'


class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    name_customer = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'customer'





class Employees(models.Model):
    id_emp = models.AutoField(primary_key=True)
    id_user = models.OneToOneField('Users', models.DO_NOTHING, db_column='id_user', blank=True, null=True)
    emp_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    salary = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'employees'


class ImportProducts(models.Model):
    id_imp = models.AutoField(primary_key=True)
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')
    import_quantity = models.IntegerField()
    import_price = models.IntegerField()
    supplier = models.CharField(max_length=100)
    import_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    import_by = models.CharField(max_length=50)
    update_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'import_products'


class LandingPages(models.Model):
    id_landing_pages = models.AutoField(primary_key=True)
    id_emp = models.ForeignKey(Employees, models.DO_NOTHING, db_column='id_emp')
    image = models.ImageField(upload_to="images/landing_pages/")
    activate = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    create_by = models.CharField(max_length=50)
    update_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'landing_pages'


class OrderProduct(models.Model):
    id_order = models.AutoField(primary_key=True)
    id_cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='id_cart')
    id_coupon = models.ForeignKey(Coupons, models.DO_NOTHING, db_column='id_coupon')
    order_description = models.TextField()
    total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_product'


class Payment(models.Model):
    status = {
        'waiting for confirmation': 'Waiting for confirmation',
        'canceled': 'Canceled',
        'confirmed': 'Confirmed',
        'delivered successfully': 'Delivered successfully'
    }
    id_payment = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(OrderProduct, models.DO_NOTHING, db_column='id_order')
    payment_status = models.BooleanField()
    order_status = models.CharField(
        max_length=50,
        choices=status
    )

    class Meta:
        managed = False
        db_table = 'payment'


class ProductCoupons(models.Model):
    id = models.AutoField(primary_key=True)
    id_coupon = models.ForeignKey(Coupons, models.DO_NOTHING, db_column='id_coupon')
    id_product = models.ForeignKey('Products', models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'product_coupons'


class Products(models.Model):
    status_product ={
        'Còn hàng':'Còn hàng',
        'Hết hàng':'Hết hàng'
    }
    id_product = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    sku = models.CharField(db_column='SKU', max_length=50, unique=True)  # Field name made lowercase.
    id_category = models.ForeignKey(Categories, models.DO_NOTHING, db_column='id_category')
    export_price = models.IntegerField()
    product_quantity = models.IntegerField()
    product_description = models.TextField(max_length=1000)
    image_product = models.ImageField(upload_to="images/image_products/")
    brand = models.CharField(max_length=200)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=255)
    activate = models.BooleanField()
    status =  models.CharField(
        max_length=50, 
        choices=status_product
    ) 
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    create_by = models.CharField(max_length=50)
    update_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'products'


class Reviews(models.Model):
    id_review = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='id_customer')
    star = models.IntegerField()
    review_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'


class Users(models.Model):
    type ={
        'employee':'employee',
        'customer':'customer'
    }
    id_user = models.AutoField(primary_key=True)
    avatar = models.ImageField(upload_to="images/image_user/")
    account_type = models.CharField(
        max_length=50, 
        choices=type
    ) 
    token = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)  # Tự động điền khi tạo
    update_at = models.DateTimeField(auto_now=True)  # Tự động điền khi cập nhật
    create_by = models.CharField(max_length=50, null=False)
    update_by = models.CharField(max_length=50, null=False)

    class Meta:
        managed = False
        db_table = 'users'


class Wishlists(models.Model):
    id_wishlist = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='id_customer')
    id_product = models.ForeignKey(Products, models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'wishlists'