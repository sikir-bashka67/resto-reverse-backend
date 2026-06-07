from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category, Menu, Order, PreOrder, Profile
from .serializers import CategorySerializer, MenuSerializer, OrderSerializer, PreOrderSerializer, ProfileSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.select_related('category').all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


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



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'items']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=True, methods=['get'], url_path='items')
    def items(self, request, pk=None):
        category = self.get_object()
        menu_items = Menu.objects.filter(category=category, is_available=True)
        serializer = MenuSerializer(menu_items, many=True)
        return Response(serializer.data)