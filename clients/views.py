from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from clients.models import Client
from clients.serializers import ClientSerializer
from rest_framework import filters


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone']
    ordering_fields = ['created_at']