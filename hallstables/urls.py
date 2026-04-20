from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HallViewSet, TableViewSet

router = DefaultRouter()
router.register(r'halls', HallViewSet)
router.register(r'tables', TableViewSet)

urlpatterns = [
    path('', include(router.urls))
]