from django.shortcuts import render


def user_registration(reqeust):
    return render(reqeust, 'account/register.html')

