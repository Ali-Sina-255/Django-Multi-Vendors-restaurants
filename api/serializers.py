from menu.models import Category, FootItem
from rest_framework import serializers
from accounts.models import User, UserProfile
from vendor.models import Vendor


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
        fields = [
            "id",
            "vendor",
            "category_name",
            "slug",
            "description",
            "created_at",
            "updated_at",
        ]


class FoodItemSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    category = CategorySerializer()

    class Meta:
        model = FootItem
        fields = [
            "food_title",
            "description",
            "price",
            "vendor",
            "category",
            "image",
            "is_available",
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
