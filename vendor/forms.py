from django import forms
from .models import Vendor


class VendorRegisterForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_licenses']
