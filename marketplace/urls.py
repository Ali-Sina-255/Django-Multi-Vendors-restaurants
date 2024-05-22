from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace_view,name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    path('add_to_cart/<int:food_id>/', views.add_to_cart_view, name='add_to_cart'),
]