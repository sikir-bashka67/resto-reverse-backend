from rest_framework import permissions, viewsets

from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('table', 'client').all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
