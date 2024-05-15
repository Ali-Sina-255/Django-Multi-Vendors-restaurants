from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.http import HttpResponse

from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from accounts.views import check_rol_vendor
from menu.models import Category, FootItem

from . forms import VendorRegisterForm 
from . models import Vendor
from menu.forms import CategoryForm, FoodItemForm
from menu.models import FootItem



def get_vendor(request):
    vendor = Vendor.objects.get(user = request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form = VendorRegisterForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings is updated')
            return redirect('vendor_profile')
        else:
            messages.error(request, 'your profile is not updated')
            print(profile_form.errors)
            print(vendor_form.errors)
            return redirect('vendor_profile')
           
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorRegisterForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        "vendor_from": vendor_form,
        "profile": profile,
        "vendor": vendor
    }
    return render(request, 'vendor/vendor_profile.html', context)


@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    return render(request, 'vendor/menu_builder.html',{
        "categories":categories
    })
    

@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def food_items_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FootItem.objects.filter(vendor=vendor, category=category)
    context = {
        "category": category,
        "food_items":food_items
    }
    return render(request, 'vendor/food_items_by_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'your category is added')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'vendor/add_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def edit_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse(f"category with is {pk} is not Found ")
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category_title = form.cleaned_data['category_name']
            category.vendor = get_vendor(request)
            category.slug = category_title
            form.save()
            messages.success(request, 'your category is update')
            return redirect('menu_builder')
        else:
            print(form.errors)
            messages.error(request,'your category is not updated')
            return redirect('edit_category')
    else:
        form = CategoryForm(instance=category)
    context = {
        "form":form, 
        "category": category
    }
    return render(request, 'vendor/edit_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'your category has been deleted successfully')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def add_food_view(request):
    if request.method == 'POST':
        form =FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, 'food item is added successfully')
            return redirect('food_items_by_category', food.category.id)
        else:
            print(form.errors)
            messages.error(request, 'your food item is not added')
            return redirect('add_food')
    else:
        form = FoodItemForm()
    context = {"form":form}
    return render(request, 'vendor/add_food.html',context)


@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def edit_food_view(request, pk=None):
    food =get_object_or_404(FootItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,'Food Item is updated')
            return redirect('food_items_by_category', food.category.id)
        else:
            print(form.errors)
            messages.error(request, 'your food is not updated')
            return redirect("edit_food", food.id)
    else:
        form = FoodItemForm(instance=food)
    context = {
        "food": food,
        "form": form
    }
    return render(request, 'vendor/edit_food.html', context)



@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def delete_food_view(request,pk):
   food = get_object_or_404(FootItem,pk=pk)
   if request.method == 'POST':
       food.delete()
       messages.success(request, 'Food Item has been deleted successfully')
       return redirect('food_items_by_category', food.category.id)
   