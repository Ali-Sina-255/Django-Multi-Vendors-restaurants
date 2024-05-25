from django import forms
from .models import Vendor, OpeningHour
from accounts.forms import allow_only_images_validator


class VendorRegisterForm(forms.ModelForm):
    vendor_licenses = forms.FileField(widget=forms.FileInput(attrs={"class":'bnt btn-info'}))
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_licenses']


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day','from_hour','to_hour','is_closed']