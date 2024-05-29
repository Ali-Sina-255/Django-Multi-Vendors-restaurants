from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import UserInForm, UserProfileForm
from accounts.models import UserProfile

# Create your views here.
login_required(login_url='login')
def customer_profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    profile_form = UserProfileForm(instance=profile)
    user_form = UserInForm()
    context = {
        "profile_form":profile_form,
        "user_form":user_form
    }
    return render(request, 'customers/c_profile.html',context)