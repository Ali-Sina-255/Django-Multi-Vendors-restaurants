from django.contrib import admin
from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    ordering = ['-date_joined']
    # FOR HASHING THE PASSWORD
    list_display_links = ('email', 'first_name')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
