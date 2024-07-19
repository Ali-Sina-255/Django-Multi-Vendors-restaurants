from django_filters import FilterSet
from accounts.models import User
from menu.models import Category , FootItem
from vendor.models import Vendor


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'category_name':['exact'],
            'vendor': ['exact']
        }
    
class UserFilterClass(FilterSet):
    class Meta:
        model = User
        fields = {
            "role": ['exact']
        
        }
        
class FoodItemFilterClass(FilterSet):
    class Meta:
        model = FootItem
        fields = {
            "food_title": ['exact'],
            'category':['exact'],
            'vendor': ['exact'],
            'price':['lt', 'gt']
        }
        
        
class VendorFilterClass(FilterSet):
    class Meta:
        model = Vendor
        fields =  {
            'user':['exact'],
            "vendor_name": ['exact'],
            "is_approved" : ['exact'],
            "update_om": ['exact']
            }