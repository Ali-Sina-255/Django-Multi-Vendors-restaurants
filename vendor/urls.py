from django.urls import path
from accounts import views as account_views
from . import views


urlpatterns = [
    path('', account_views.vendor_dashboard_view, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),

    ]