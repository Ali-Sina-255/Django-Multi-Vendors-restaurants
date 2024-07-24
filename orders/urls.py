from django.urls import path
from . import views

urlpatterns = [
    path('order_place/',views.order_place_view, name='order_place'),
    path('payments/',views.payments, name='payments'),
]
