from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_registration, name='register'),
    path('register_vendor/', views.register_vendor, name='register_vendor'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customer_dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('vendor_dashboard/', views.vendor_dashboard_view, name='vendor_dashboard'),
    path('my_account/', views.my_account_view, name='my_account'),
]
