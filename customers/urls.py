from django.urls import path
from .  import views

urlpatterns = [
    path('profile/', views.customer_profile_view, name='c_profile')
]
