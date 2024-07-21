from menu.models import Category, FootItem
from rest_framework import serializers
from accounts.models import User, UserProfile
from vendor.models import Vendor
from marketplace.models import Cart
from django.db.models import Sum, F


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "user",
            "user_profile",
            "vendor_name",
            "vendor_slug",
            "vendor_licenses",
            "is_approved",
            "update_om",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['vendor', 'category_name', 'slug', 'description', 'created_at', 'updated_at']

class FoodItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = FootItem
        fields = ['vendor', 'category', 'food_title', 'description', 'price', 'image', 'is_available', 'created_at', 'updated_at']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        vendor = validated_data.get('vendor')  # Get the vendor from the FoodItem
        category_data['vendor'] = vendor  # Set the vendor for the Category
        category, created = Category.objects.get_or_create(**category_data)
        food_item = FootItem.objects.create(category=category, **validated_data)
        return food_item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    food_item = FoodItemSerializer()
    total_food_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'food_item', 'quantity', 'updated_at', 'total_food_items', 'total_price']

    def get_total_food_items(self, obj):
        total_food_items = Cart.objects.aggregate(total_items=Sum('quantity'))['total_items']
        return total_food_items

    def get_total_price(self, obj):
        total_price = Cart.objects.aggregate(
            total_price=Sum(F('quantity') * F('food_item__price'))
        )['total_price']
        return total_price