from django.contrib import admin
from . models import Cart

class CartAdminModel(admin.ModelAdmin):
    list_display = ['user','food_item','quantity','updated_at']
admin.site.register(Cart, CartAdminModel)
