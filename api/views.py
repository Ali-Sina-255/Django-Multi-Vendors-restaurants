from accounts.models import User, UserProfile
from . serializers import CategorySerializer, FoodItemSerializer, UserSerializer, UserProfileSerializer, VendorSerializer
from rest_framework import status
from menu.models import Category, FootItem
from vendor.models import Vendor

from rest_framework.viewsets import ModelViewSet


class CategoryApiViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class FoodItemApiViewSet(ModelViewSet):
    queryset = FootItem.objects.all()
    
    def get_serializer_class(self):
        return FoodItemSerializer
    

class UserApiViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileAPiViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()     
    serializer_class = UserProfileSerializer
    
class VendorApiViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    