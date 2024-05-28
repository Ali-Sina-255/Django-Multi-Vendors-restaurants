from django.shortcuts import render

# Create your views here.
def customer_profile_view(request):
    return render(request, 'customers/c_profile.html')