from django.contrib import admin
from home.models import *  # Import tất cả các models
# Lấy danh sách tất cả các models trong ứng dụng hiện tại
# models = apps.get_models()

# # Đăng ký từng model vào Django admin
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass  # Bỏ qua nếu model đã được đăng ký trước đó



admin.site.register(Products)
admin.site.register(OrderProduct)
admin.site.register(Wishlists)
admin.site.register(Reviews)
admin.site.register(ProductCoupons)
admin.site.register(Payment)
admin.site.register(Users)
admin.site.register(Employees)
admin.site.register(LandingPages)
admin.site.register(ImportProducts)
admin.site.register(Customer)
admin.site.register(Coupons)
admin.site.register(Categories)
admin.site.register(CartDetail)
admin.site.register(Cart)
