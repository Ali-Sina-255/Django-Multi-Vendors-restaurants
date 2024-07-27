import json
from django.db import models
from accounts.models import User
from menu.models import FootItem
from vendor.models import Vendor
 
 
request_object = ""


PAYMENT_METHOD = (
    ('Paypal', 'PayPal'),
)
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD,max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction_id
    
class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Complete", "Complete"),
        ("Accepted", "Accepted"),
        ("Cancelled", "Cancelled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)  # Remove unique=True
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    total = models.FloatField()
    total_data = models.JSONField(blank=True, null=True)
    payment_method = models.CharField(max_length=200)
    status = models.CharField(choices=STATUS, max_length=30, default='New')
    is_order = models.BooleanField(default='False')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        if self.total_data:
            total_data = json.loads(self.total_data)
            data  = total_data.get(str(vendor.id))
            print(data)
        return vendor
    
    
    def __str__(self) -> str:
        return self.order_number

    def order_place_to(self):
        return ",".join([str(i) for i in self.vendors.all()])



class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FootItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_item.food_title