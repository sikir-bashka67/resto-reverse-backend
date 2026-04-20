from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, CategoryViewSet, OrderViewSet, PreOrderViewSet

router = DefaultRouter()
router.register(r'menu', MenuViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'preorders', PreOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]