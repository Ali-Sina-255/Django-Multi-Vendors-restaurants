from django.urls import path
from . import views



urlpatterns = [
    path('', views.marketplace_view,name='marketplace')
]