from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Menu, Category, Profile, Order, PreOrder
from .serializers import MenuSerializer, CategorySerializer, ProfileSerializer, OrderSerializer, PreOrderSerializer


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
        return Profile.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(profile__user=self.request.user).select_related('profile')

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile) # type: ignore


class PreOrderViewSet(viewsets.ModelViewSet):
    queryset = PreOrder.objects.all()
    serializer_class = PreOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PreOrder.objects.filter(profile__user=self.request.user).select_related('profile')

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile) # type: ignore