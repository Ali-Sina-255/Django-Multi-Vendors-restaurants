from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_registration, name='register'),
    path('register_vendor/', views.register_vendor, name='register_vendor'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
