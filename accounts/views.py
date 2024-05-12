from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from .forms import UserRegistrationForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorRegisterForm
from .utils import detect_user, send_verification_email, send_reset_password_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator


# Restrict the vendor from accessing the customers page
def check_rol_vendor(user):
    if user.role == 1:
        return True
    raise PermissionDenied


# Restrict the vendor from accessing the customers page
def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied


def user_registration(reqeust):
    if reqeust.user.is_authenticated:
        messages.warning(reqeust, 'your are already registered')
        return redirect('my_account')

    elif reqeust.method == 'POST':
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
            # send the verification email
            mail_subject = 'Reset your password'
            email_template = 'account/email/verification_email.html'
            send_verification_email(reqeust, user, mail_subject, email_template)

            messages.success(reqeust, 'Your registration was successfully')
            user.redirect('home')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(reqeust, 'account/register.html', context)


def register_vendor(reqeust):
    if reqeust.user.is_authenticated:
        messages.warning(reqeust, 'your are already registered')
        return redirect('my_account')

    elif reqeust.method == 'POST':
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

            # send the verification email
            mail_subject = 'Reset your password'
            email_template = 'account/email/verification_email.html'
            send_verification_email(reqeust, user, mail_subject, email_template)

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


def activate(reqeust, uidb64, token):
    # activated the user by settings the is_active to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(reqeust, 'congratulation your account is activated')
        return redirect('my_account')
    else:
        messages.error(reqeust, 'Invalid Activation links')
        return redirect('my_account')
    return render()


def login_view(reqeust):
    if reqeust.user.is_authenticated:
        messages.warning(reqeust, 'You are already logged in')
        return redirect('my_account')

    elif reqeust.method == 'POST':
        email = reqeust.POST.get('email')
        password = reqeust.POST.get('password')
        user = auth.authenticate(reqeust, email=email, password=password)
        if user is not None:
            auth.login(reqeust, user)
            messages.success(reqeust, 'You are now logged in')
            return redirect('my_account')
        else:
            messages.error(reqeust, 'Invalid Credentials')
            return redirect('login')
    return render(reqeust, 'account/login.html')


def logout_view(reqeust):
    auth.logout(reqeust)
    messages.error(reqeust, 'you are logged out now')
    return redirect('login')


def forgot_password_view(reqeust):
    if reqeust.method == 'POST':
        email = reqeust.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)
            mail_subject = 'Reset your password'
            email_template = 'account/email/reset_password_email.html'
            send_verification_email(reqeust, user, mail_subject, email_template)
            # send_reset_password_email(reqeust, user)
            messages.success(reqeust, 'Your password reset link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(reqeust, 'Account does not exist')
            return redirect('forgot_password')

    return render(reqeust, 'account/forgot_password.html')


def reset_password_validate_view(reqeust, uidb64, token):
    # Validate the user by decoding the token and user primary key
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        reqeust.session['uid'] = uid
        messages.info('please reset your password')
        return redirect('reset_password')
    else:
        messages.error(reqeust, 'this link has been expired')
        return redirect('my_account')


def reset_password_view(reqeust):
    if reqeust.method == 'POST':
        password = reqeust.POST['password']
        confirm_password = reqeust.POST['confirm_password']

        if password == confirm_password:
            pk = reqeust.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.asave()
            messages.success('your password has been reset successfully')
            return redirect('login')

        else:
            messages.error(reqeust, 'password dont match')
            return redirect('reset_password')

    return render(reqeust, 'account/reset_password.html')


@login_required(login_url='login')
def my_account_view(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


@login_required(login_url='login')
@user_passes_test(check_rol_vendor)
def vendor_dashboard_view(reqeust):
    return render(reqeust, 'account/vendor_dashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard_view(reqeust):
    return render(reqeust, 'account/customer_vendor_dashboard.html')
