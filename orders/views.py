from django.shortcuts import render

# Create your views here.
def order_place_view(request):
    return render(request, 'order/order_place.html')