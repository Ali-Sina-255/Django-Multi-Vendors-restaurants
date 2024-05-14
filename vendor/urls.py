from django.urls import path
from accounts import views as account_views
from . import views


urlpatterns = [
    path('', account_views.vendor_dashboard_view, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/category/<int:pk>/', views.food_items_by_category, name='food_items_by_category'),
    path('menu_builder/add_category/', views.add_category, name='add_category'),
    path('menu_builder/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete_category/edit/<int:pk>/', views.delete_category, name='delete_category'),
    
    # CRUD Food Items 
    path('menu_builder/add_food/', views.add_food_view, name='add_food'),
    
    
    
]  