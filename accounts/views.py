from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User
from django.contrib import messages, auth


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
    return render(reqeust, 'account/register_restaurant.html')


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
