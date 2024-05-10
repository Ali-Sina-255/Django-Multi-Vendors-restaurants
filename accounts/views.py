from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User


def user_registration(reqeust):
    if reqeust.method == 'POST':
        form = UserRegistrationForm(reqeust.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            return redirect('home')
        # scode way for hashing password
        #     first_name = form.cleaned_data['first_name']
        #     last_name = form.cleaned_data['last_name']
        #     email = form.cleaned_data['email']
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password']
        #     user = User.objects.create_user(
        #         first_name=first_name,
        #         last_name=last_name,
        #         username=username,
        #         email=email)
        #     user.role = User.Customer
        #     user.save()
        #     user.redirect('home')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form': form}

    return render(reqeust, 'account/register.html', context)
