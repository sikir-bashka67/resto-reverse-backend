from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from .models import Category, Menu, Order, PreOrder, Profile
from .serializers import CategorySerializer, MenuSerializer, OrderSerializer, PreOrderSerializer, ProfileSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.select_related('category').all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user).select_related('user')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user', 'table', 'booking').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PreOrderViewSet(viewsets.ModelViewSet):
    queryset = PreOrder.objects.select_related('user', 'booking').all()
    serializer_class = PreOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
