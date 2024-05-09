
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("FoodOnline.urls")),
    path("account/", include("accounts.urls")),
]
