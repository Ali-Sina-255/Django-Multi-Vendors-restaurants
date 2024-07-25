from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required


from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from accounts.utils import send_notification
from . forms import OrderForms
from . models import Order, Payment, OrderedFood
from . utils import generate_order_num


# Create your views here.
@login_required(login_url='login')
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

@login_required(login_url='login')
def payments(request):
    # if the request is ajax or not 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')
        
        order = Order.objects.get(user=request.user,order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount = order.total,
            status=status
        )
        payment.save()
        order.payment   = payment
        order.is_order=True
        order.save()
        
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.food_item = item.food_item
            ordered_food.quantity = item.quantity
            ordered_food.price = item.food_item.price
            ordered_food.amount = item.food_item.price * item.quantity
            ordered_food.save()
        mail_subject = 'Thank your for ordering with US.'
        mail_template = 'order/email/order_confirmation_email.html'
        context = {
            'user':request.user,
            'order':order,
            'to_email':order.email
        }
        # send notification email to customer
        send_notification(mail_subject,mail_template,context)
        
        #   SEND NOTIFICATION EMAIL TO VENDOR
        
        mail_subject = "You have received new order"
        mail_template = 'order/email/order_received_email.html'
        
        to_email = []
        for i in cart_items:
            if i.food_item.vendor.user.email is not to_email:   
                to_email.append(i.food_item.vendor.user.email)
        print(to_email)
            
        context = {
            "order":order,
            "to_email":to_email,
        }
        send_notification(mail_subject,mail_template,context)
    # cart_items.delete()
    response = {
        'order_number': order_number,
        'transaction_id': transaction_id
    }
    return JsonResponse(response)
        # update the order 
        
        # store the payment detail in the payment model 
        # update the order model 
        # movie the cart item to order food model 


def order_complete_view(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get("trans_id")
    try:
        order = Order.objects.get(order_number=order_number, transaction_id=transaction_id,is_order=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal +=(item.price * item.quantity)
        context = {
            'order':order,
            "ordered_food":ordered_food,
            "subtotal":subtotal
        }
        return render(request, 'order/order_complete.html', context) 
        
    except:
        return redirect('home')