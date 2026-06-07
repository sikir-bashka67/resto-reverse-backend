from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from booking.models import Booking
from .models import Hall, Table
from .serializers import HallSerializer, TableSerializer

CLEANUP_INTERVAL = timedelta(minutes=settings.BOOKING_CLEANUP_INTERVAL_MINUTES)


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminUser]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.select_related('hall').filter(is_deleted=False)
    serializer_class = TableSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'], url_path='available', permission_classes=[IsAuthenticated])
    def available(self, request):
        starting_at = request.query_params.get('starting_at')
        ending_at = request.query_params.get('ending_at')

        if not starting_at or not ending_at:
            return Response(
                {'detail': 'Передайте starting_at и ending_at как query параметры.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from django.utils.dateparse import parse_datetime
            starting_at = parse_datetime(starting_at)
            ending_at = parse_datetime(ending_at)
            if not starting_at or not ending_at:
                raise ValueError
        except ValueError:
            return Response({'detail': 'Неверный формат даты.'}, status=status.HTTP_400_BAD_REQUEST)

        booked_table_ids = Booking.objects.filter(
            starting_at__lt=ending_at + CLEANUP_INTERVAL,
            ending_at__gt=starting_at - CLEANUP_INTERVAL,
        ).exclude(status='cancelled').values_list('table_id', flat=True)

        tables = Table.objects.select_related('hall').filter(
            is_deleted=False,
            status='available',
        ).exclude(id__in=booked_table_ids)

        serializer = self.get_serializer(tables, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='qr-info', permission_classes=[IsAuthenticated])
    def qr_info(self, request, pk=None):
        table = self.get_object()
        return Response({
            'table_id': table.pk,
            'table_name': table.name,
            'hall': table.hall.name,
            'seats': table.seats,
            'type': table.type,
            'status': table.status,
            'qr_code': request.build_absolute_uri(table.qr_code.url) if table.qr_code else None,
        })

    @action(detail=True, methods=['patch'], url_path='status')
    def set_status(self, request, pk=None):
        table = self.get_object()
        new_status = request.data.get('status')

        valid_statuses = [s[0] for s in Table.STATUS_CHOICES]
        if not new_status:
            return Response({'detail': 'Передайте status.'}, status=status.HTTP_400_BAD_REQUEST)
        if new_status not in valid_statuses:
            return Response(
                {'detail': f'Недопустимый статус. Допустимые: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        table.status = new_status
        table.save(update_fields=['status'])
        return Response({'status': table.status})

    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        table = self.get_object()

        now = timezone.now()
        active_booking = Booking.objects.filter(
            table=table,
            status='guest_arrived',
            starting_at__lte=now,
            ending_at__gte=now,
        ).first()

        if not active_booking:
            return Response(
                {'detail': 'Нет активной брони на этом столе.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        active_booking.transition_to('completed')

        table.status = 'available'
        table.save(update_fields=['status'])

        return Response({
            'detail': 'Стол освобождён.',
            'booking_id': active_booking.pk,
            'table': table.name,
        })