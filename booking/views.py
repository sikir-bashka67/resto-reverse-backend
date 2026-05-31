from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('table', 'client').all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def my_bookings(self, request):
        bookings = self.queryset.filter(client__user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='today')
    def today_bookings(self, request):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)

        bookings = self.queryset.filter(
            starting_at__range=(today_start, today_end)
        ).exclude(status='cancelled')

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.client.user != request.user and not request.user.is_staff:
            return Response({'detail': 'У вас нет прав на отмену этой брони'}, status=status.HTTP_403_FORBIDDEN)

        if booking.status == 'cancelled':
            return Response({'detail': 'Бронирование уже отменено'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'Бронирование успешно отменено'})