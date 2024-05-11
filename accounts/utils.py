from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def detect_user(user):
    if user.role == 1:
        redirect_url = 'vendor_dashboard'
        return redirect_url
    elif user.role == 2:
        redirect_url = 'customer_dashboard'
        return redirect_url
    elif None == user.role and user.is_admin:
        redirect_url = '/admin'
        return redirect_url


def send_verification_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'please activate your account'
    message = render_to_string('account/email/verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(email_subject, message, to=[to_email])
    mail.send()

