from django.db import transaction
from django.utils import timezone
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from hallstables.models import Table
from .models import Booking
from .serializers import BookingSerializer
from datetime import timedelta
from django.conf import settings
from booking.tasks import send_booking_reminder

CLEANUP_INTERVAL = timedelta(minutes=settings.BOOKING_CLEANUP_INTERVAL_MINUTES)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('table', 'client').all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.select_related('table', 'client').all()
        return Booking.objects.select_related('table', 'client').filter(client__user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            table = serializer.validated_data['table']
            starting_at = serializer.validated_data['starting_at']
            ending_at = serializer.validated_data['ending_at']

            Table.objects.select_for_update().get(pk=table.pk)

            overlap = Booking.objects.filter(
                table=table,
                starting_at__lt=ending_at + CLEANUP_INTERVAL,
                ending_at__gt=starting_at - CLEANUP_INTERVAL,
            ).exclude(status='cancelled')

            if overlap.exists():
                raise ValidationError({'table': 'Этот стол уже забронирован на выбранное время.'})

            booking = serializer.save()

            reminder_time = booking.starting_at - timedelta(hours=2)
            send_booking_reminder.apply_async(
                args=[booking.pk],
                eta=reminder_time,
            )

    @action(detail=False, methods=['get'], url_path='me')
    def my_bookings(self, request):
        bookings = self.get_queryset().filter(client__user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='today')
    def today_bookings(self, request):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timezone.timedelta(days=1)

        bookings = self.get_queryset().filter(
            starting_at__range=(today_start, today_end)
        ).exclude(status='cancelled')

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.client.user != request.user and not request.user.is_staff:
            return Response({'detail': 'У вас нет прав на отмену этой брони'}, status=status.HTTP_403_FORBIDDEN)

        try:
            booking.transition_to('cancelled')
        except ValidationError as e:
            return Response({'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Бронирование успешно отменено'})

    @action(detail=False, methods=['post'], url_path='check-in', permission_classes=[permissions.IsAdminUser])
    def check_in(self, request):
        qr_token = request.data.get('qr_token')
        if not qr_token:
            return Response({'detail': 'QR токен не передан.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.select_related('client', 'table').get(qr_token=qr_token)
        except Booking.DoesNotExist:
            return Response({'detail': 'Бронирование не найдено.'}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()
        if not (booking.starting_at <= now <= booking.ending_at):
            return Response({'detail': 'Время бронирования ещё не наступило или уже истекло.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            booking.transition_to('guest_arrived')
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 'Гость зарегистрирован.',
            'booking_id': booking.pk,
            'client': booking.client.name,
            'table': booking.table.name,
        })