from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

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
 
    def save(self,*args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'account/email/admin_approved.html'
                context = {
                    "user": self.user,
                    "is_approved":self.is_approved
                }
                if self.is_approved == True:
                    mail_subject = 'Congratulation Your restaurant has been approved'
                    send_notification(mail_subject, mail_template , context)
                else:
                    mail_subject = "we're  sorry, you are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template , context)
        return super(Vendor, self).save(*args, **kwargs)