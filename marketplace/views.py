from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from menu.models import Category, FootItem
from vendor.models import Vendor
from marketplace.models import Cart
from . context_processors import get_cart_counter, get_cart_amounts


# Create your views here.
@login_required(login_url='login')
def marketplace_view(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        "vendors":vendors,
        "vendor_count":vendor_count
    }
    return render(request, 'marketplace/listing.html',context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch("fooditems",
                queryset=FootItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
       
    else:
        cart_item = 0

    context = {
        "vendor": vendor, 
        "categories":categories,
        "cart_item":cart_item
    }
    return render(request,'marketplace/vendor_detail.html',context)


def add_to_cart_view(request,food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item is exist in the cart
            try:
                food_item = FootItem.objects.get(id=food_id)
                print(food_item)
                # if the user is already added to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, food_item=food_item)
                    # increase the cart item 
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({"status":"success","message":"Increased the cart quantity", "cart_counter":get_cart_counter(request), 'qty':check_cart.quantity, "cart_amount":get_cart_amounts(request)})

                except:
                    check_cart = Cart.objects.create(user=request.user, food_item=food_item, quantity=1)
                    return JsonResponse({'status':"Success","message":"added to the card item","cart_counter":get_cart_counter(request),'qty':check_cart.quantity, "cart_amount":get_cart_amounts(request)})
                
            except:
                return JsonResponse({"status":"Failed", 'message':'this food does not exist!'})

        else:

            return JsonResponse({"status":"Failed","message":"Invalid Request"})
    
    return JsonResponse({'status':"login_required", 'message':'Please login to continue'})


def decrease_cart_view(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item is exist in the cart
            try:
                food_item = FootItem.objects.get(id=food_id)
                print(food_item)
                # if the user is already added to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, food_item=food_item)
                    # decrease the cart item 
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({"status":"success", "cart_counter":get_cart_counter(request), 'qty':check_cart.quantity})

                except:
                    return JsonResponse({'status':"Failed","message":"You don't have this item in your cart"})
                
            except:
                return JsonResponse({"status":"Failed", 'message':'this food does not exist!'})

        else:

            return JsonResponse({"status":"Failed","message":"Invalid Request"})
    
    return JsonResponse({'status':"login_required", 'message':'Please login to continue'})


def cart_view(request):
    cart_item = Cart.objects.filter(user=request.user).order_by('-created_at')
    context = {"cart_item":cart_item}
    return render(request, 'marketplace/cart.html', context)

@login_required(login_url='login')
def delete_cart_view(request, cart_id):
     if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status":"success","message":"cart item has been deleted","cart_counter":get_cart_counter(request)})
            except:
                return JsonResponse({"status":"Failed", 'message':'this food does not exist!'})

        else:
            return JsonResponse({"status":"Failed","message":"Invalid Request"})
        



