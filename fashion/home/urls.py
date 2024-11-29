from django.urls import path

from home import views

urlpatterns = [
    path('dashboard/', views.admin, name='dashboard'),
    path('login_admin/', views.admin_login, name='login_admin'),
    # path('import_product', views.import_products, name='import_products')
]
