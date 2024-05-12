from django.shortcuts import render


def vendor_profile(request):
    return render(request, 'vendor/vendor_profile.html')
