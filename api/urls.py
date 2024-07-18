from django.urls import path
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()

router.register('user', views.UserApiViewSet)
router.register('user/profile', views.UserProfileAPiViewSet)
router.register('category', views.CategoryApiViewSet)
router.register('food-item', views.FoodItemApiViewSet)
router.register('vendor', views.VendorApiViewSet)
urlpatterns = router.urls