from django.db import models
from accounts.models import User, UserProfile


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_profile')
    vendor_name = models.CharField(max_length=255)
    vendor_licenses = models.ImageField(upload_to='vendor/licenses')
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    update_om = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
