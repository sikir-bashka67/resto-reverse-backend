from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Hall, Table
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import HallSerializer, TableSerializer


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminUser]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.select_related('hall').all()
    serializer_class = TableSerializer
    permission_classes = [IsAdminUser]

    # @action(detail=False, methods=['get'], url_path='available')
    # def available(self, request):
    #     return Response()
    #
    # @action(detail=True, methods=['get'], url_path='qr-info')
    # def qr_info(self, request, pk=None):
    #     return Response()
    #
    # @action(detail=True, methods=['patch'], url_path='status')
    # def status(self, request, pk=None):
    #     return Response()
    #
    # @action(detail=True, methods=['post'], url_path='checkout')
    # def checkout(self, request, pk=None):
    #     return Response()