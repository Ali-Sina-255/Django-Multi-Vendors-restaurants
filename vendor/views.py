from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.http import HttpResponse, JsonResponse

from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from accounts.views import check_rol_vendor
from menu.models import Category, FootItem
from orders.models import Order, OrderedFood

from .forms import VendorRegisterForm, OpeningHoursForm
from .models import Vendor, OpeningHour
from menu.forms import CategoryForm, FoodItemForm
from menu.models import FootItem

def get_vendor(request):
    vendors = Vendor.objects.filter(user=request.user)
    if vendors.count() == 1:
        return vendors.first()
    elif vendors.count() > 1:
        # Handle the case where multiple vendors are found
        # For example, return the first one or raise an error
        return vendors.first()  # or handle it differently
    else:
        return None


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorRegisterForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Settings is updated")
            return redirect("vendor_profile")
        else:
            messages.error(request, "your profile is not updated")
            print(profile_form.errors)
            print(vendor_form.errors)
            return redirect("vendor_profile")

    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorRegisterForm(instance=vendor)
    context = {
        "profile_form": profile_form,
        "vendor_from": vendor_form,
        "profile": profile,
        "vendor": vendor,
    }
    return render(request, "vendor/vendor_profile.html", context)


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    return render(request, "vendor/menu_builder.html", {"categories": categories})


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def food_items_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FootItem.objects.filter(vendor=vendor, category=category)
    context = {"category": category, "food_items": food_items}
    return render(request, "vendor/food_items_by_category.html", context)


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, "your category is added")
            return redirect("menu_builder")
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    context = {"form": form}
    return render(request, "vendor/add_category.html", context)


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def edit_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse(f"category with is {pk} is not Found ")
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category_title = form.cleaned_data["category_name"]
            category.vendor = get_vendor(request)
            category.slug = category_title
            form.save()
            messages.success(request, "your category is update")
            return redirect("menu_builder")
        else:
            print(form.errors)
            messages.error(request, "your category is not updated")
            return redirect("edit_category")
    else:
        form = CategoryForm(instance=category)

    context = {"form": form, "category": category}
    return render(request, "vendor/edit_category.html", context)


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "your category has been deleted successfully")
    return redirect("menu_builder")



@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def add_food_view(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            vendor = get_vendor(request)
            if not vendor:
                messages.error(request, "No vendor found for this user.")
                return redirect("add_food")
            food.vendor = vendor
            food.slug = slugify(food_title)
            food.save()
            messages.success(request, "Food item is added successfully")
            return redirect("food_items_by_category", food.category.id)
        else:
            print(form.errors)
            messages.error(request, "Your food item is not added")
            return redirect("add_food")
    else:
        form = FoodItemForm()
        form.fields["category"].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {"form": form}
    return render(request, "vendor/add_food.html", context)

@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def edit_food_view(request, pk=None):
    food = get_object_or_404(FootItem, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, "Food Item is updated")
            return redirect("food_items_by_category", food.category.id)
        else:
            print(form.errors)
            messages.error(request, "your food is not updated")
            return redirect("edit_food", food.id)
    else:
        form = FoodItemForm(instance=food)
        form.fields["category"].queryset = Category.objects.filter(
            vendor=get_vendor(request)
        )

    context = {"food": food, "form": form}
    return render(request, "vendor/edit_food.html", context)


@login_required(login_url="login")
@user_passes_test(check_rol_vendor)
def delete_food_view(request, pk):
    food = get_object_or_404(FootItem, pk=pk)
    if request.method == "POST":
        food.delete()
        messages.success(request, "Food Item has been deleted successfully")
        return redirect("food_items_by_category", food.category.id)


def opening_hours_view(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHoursForm()
    context = {"form": form, "opening_hours": opening_hours}
    return render(request, "vendor/opening_hours.html", context)


def add_opening_hour_view(request):
    if request.user.is_authenticated:
        if (request.headers.get("x-requested-with") == "XMLHttpRequest"
            and request.method == "POST"):
            day = request.POST.get("day")
            from_hour = request.POST.get("from_hour")
            to_hour = request.POST.get("to_hour")
            is_closed = request.POST.get("is_closed")

            try:
                hour = OpeningHour.objects.create(
                    vendor=get_vendor(request),
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed,
                )
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {
                            "status": "success",
                            "id": hour.id,
                            "day": day.get_day_display(),
                            "is_closed": "Closed",
                        }
                    else:
                        response = {
                            "status": "success",
                            "id": hour.id,
                            "day": day.get_day_display(),
                            "from_hour": hour.from_hour,
                            "to_hour": hour.to_hour,
                        }
                return JsonResponse(response)
            except IntegrityError as e:
                response = {
                    "status": "failed",
                    "message": from_hour
                    + "-"
                    + to_hour
                    + " already exists for this day!",
                }
                return JsonResponse(response)
        else:
            HttpResponse("invalid Request")


def remove_opening_hour_view(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            return JsonResponse({"status": "success", "id": pk})


def review_view(request, restaurant_id):
    pass


def vendor_order_details_view(request ,order_number):
    try:
        order = Order.objects.get(order_number=order_number,is_order=True)
        ordered_food = OrderedFood.objects.filter(order=order,food_item__vendor=get_vendor(request))
    
        context = {
            "order":order,
            "ordered_food":ordered_food,
            "subtotal":order.get_total_by_vendor()['subtotal'],
            "total":order.get_total_by_vendor()["grand_total"]
        }
        return render(request, 'vendor/vendor_order_detail.html',context)   
    except:
        return redirect('vendor')


def my_order_view(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_order=True)

    context = {
        "orders":orders
    }
    return render(request, 'vendor/my_order.html', context)