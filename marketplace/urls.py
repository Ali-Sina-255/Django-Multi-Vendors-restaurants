from django.urls import path
from . import views



urlpatterns = [
    path('', views.marketplace_view,name='marketplace'),
    path('<slug:vendor_slug>/', views.market_palce_detail, name='vendor_detail')
]