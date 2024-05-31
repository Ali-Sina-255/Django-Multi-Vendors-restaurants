
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as marketplace_view
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("FoodOnline.urls")),
    path("accounts/", include("accounts.urls")),
    path('cart/',marketplace_view.cart_view,name='cart'),
    path('search/',marketplace_view.search_view,name='search'),
    path('checkout/',marketplace_view.checkout_view,name='checkout'),
    path("marketplace/", include("marketplace.urls")),
    path("customers/", include("customers.urls")),
    path('order/',include('orders.urls'))
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
