# from django.urls import path
from rest_framework.routers import DefaultRouter

from api_admin import views

router = DefaultRouter()

router.register(r'category', views.CategoryViewSet, basename="categories")
router.register(r'product', views.ProductViewSet, basename="products")

urlpatterns = router.urls
