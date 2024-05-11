from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorRegisterForm


def user_registration(reqeust):
    if reqeust.method == 'POST':
        form = UserRegistrationForm(reqeust.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email)
            user.role = User.Customer
            user.save()
            messages.success(reqeust, 'Your registration was successfully')
            user.redirect('home')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(reqeust, 'account/register.html', context)


def register_vendor(reqeust):
    if reqeust.method == 'POST':
        form = UserRegistrationForm(reqeust.POST)
        vendor_form = VendorRegisterForm(reqeust.POST, reqeust.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(reqeust,
                             'Your restaurant registration has been registered  successfully! please with for the '
                             'approval.')
            return redirect('register_vendor')
        else:
            messages.error(reqeust, 'Registration was not registered successfully')
            return redirect('register_vendor')
            print(form.errors)
            print(vendor_form.errors)
    else:
        form = UserRegistrationForm()
        vendor_form = VendorRegisterForm()
    context = {
        'form': form,
        'vendor_form': vendor_form,

    }
    return render(reqeust, 'account/register_restaurant.html', context)


def login_view(reqeust):
    if reqeust.method == 'POST':
        email = reqeust.POST.get('email')
        password = reqeust.POST.get('password')
        user = auth.authenticate(reqeust, email=email, password=password)
        if user is not None:
            auth.login(reqeust, user)
            messages.success(reqeust, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(reqeust, 'Invalid Credentials')
            return redirect('login')
    return render(reqeust, 'account/login.html')


def logout_view(reqeust):
    auth.logout(reqeust)
    messages.error(reqeust, 'you are logged out now')
    return redirect('login')


def dashboard_view(reqeust):
    return render(reqeust, 'account/dashboard.html')
