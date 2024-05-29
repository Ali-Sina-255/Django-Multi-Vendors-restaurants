from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserInForm, UserProfileForm
from accounts.models import UserProfile,User
from django.contrib import messages

# Create your views here.
login_required(login_url='login')
def customer_profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES,instance=profile)
        user_form = UserInForm(request.POST,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save() 
            messages.success(request, 'your profile is updated successfully')
            return redirect('c_profile')
        else:
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, 'your profile is not updated')
            return redirect('c_profile')
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInForm(instance=request.user)
    context = {
        "profile_form":profile_form,
        "user_form":user_form,
        "profile":profile
    }
    return render(request, 'customers/c_profile.html',context)