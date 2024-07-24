from django.shortcuts import render, redirect
from django.contrib import messages
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts

from . forms import OrderForms
from . models import Order, Payment
from . utils import generate_order_num



# Create your views here.
def order_place_view(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('marketplace')
    
    subtotal = get_cart_amounts(request)['subtotal']
    grand_total = get_cart_amounts(request)['grand_total']
    if request.method == "POST":
        form = OrderForms(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone_number = form.cleaned_data['phone_number']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.user = request.user
            order.total = grand_total
            order.payment_method  = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_num(order.id)
            order.save()
            messages.success(request, 'your order is send successfully')
            context ={
                "order":order,
                "cart_items":cart_items
            }
            return render(request, 'order/order_place.html', context)
           
        else:
            print(form.errors)
            messages.error(request, 'your order is not send successfully!')

        print(subtotal,grand_total)
    return render(request, 'order/order_place.html')

 
def payments(request):
    # if the request is ajax or not 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment.objects.get(user=request.user,
                                      transaction_id=transaction_id,
                                      payment_method = payment_method,
                                      amount = order.id,
                                      status = status
                                      )
        payment.save()
        # update the order 
        order.payment = payment
        order.is_order = True
        order.save()

        # store the payment detail in the payment model 
        # update the order model 
        # movie the cart item to order food model 

    