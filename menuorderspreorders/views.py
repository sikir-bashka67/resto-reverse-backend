from rest_framework import viewsets
from .models import Menu, Category, Order, PreOrder
from .serializers import MenuSerializer, CategorySerializer, OrderSerializer, PreOrderSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PreOrderViewSet(viewsets.ModelViewSet):
    queryset = PreOrder.objects.all()
    serializer_class = PreOrderSerializer