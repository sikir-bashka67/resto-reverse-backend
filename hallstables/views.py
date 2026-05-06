from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Hall, Table
from .serializers import HallSerializer, TableSerializer


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAuthenticated]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.select_related('hall').all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]