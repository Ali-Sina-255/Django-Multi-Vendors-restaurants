from django.shortcuts import render, redirect
from django.contrib import messages
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts

from . forms import OrderForms
from . models import Order

# Create your views here.
def order_place_view(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    subtotal = get_cart_amounts(request)['subtotal']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['']
    if request.method == "POST":
        form = OrderForms(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone_number = form.cleaned_data['phone_number']
            order.email= form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.total = grand_total
            order.tax_data = tax_data
            order.payment_method = request.POST['payment_method']
            order.order_number = '255'
            order.save()
            messages.success(request, 'your order is send successfully')
            return redirect('place_order')
        else:
            print(form.errors)
            messages.error(request, 'your order is not send successfully!')
    print(subtotal,grand_total)
    return render(request, 'order/order_place.html')