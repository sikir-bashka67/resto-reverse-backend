from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from staff.models import Staff
from staff.serializers import StaffSerializer
from rest_framework import filters


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone']
    ordering_fields = ['created_at']