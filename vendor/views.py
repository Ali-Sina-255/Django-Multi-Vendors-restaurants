from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse

from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from accounts.views import check_rol_vendor
from menu.models import Category

from . forms import VendorRegisterForm
from . models import Vendor

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


def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor)
    return render(request, 'vendor/menu_builder.html',{
        "categories":categories
    })