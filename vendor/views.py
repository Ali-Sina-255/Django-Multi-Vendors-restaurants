from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse

from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from accounts.views import check_rol_vendor

from . forms import VendorRegisterForm
from . models import Vendor

@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    try:
        vendor = Vendor.objects.get(user = request.user)
    except: 
        return HttpResponse('not found ')

    # vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form = VendorRegisterForm(request.POST,request.FILES)
        if profile_form.is_valid() and vendor_profile.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings is updated')
            return redirect('vendor_profile')
        else:
            messages.error(request, 'your profile is not updated')
            return redirect('vendor_profile')
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorRegisterForm()
    context = {
        'profile_form': profile_form,
        "vendor_from": vendor_form
    }
    return render(request, 'vendor/vendor_profile.html', context)
