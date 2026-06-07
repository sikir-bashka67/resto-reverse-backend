from django.utils import timezone
from rest_framework import serializers
from booking.models import Booking
from datetime import timedelta
from django.conf import settings

CLEANUP_INTERVAL = timedelta(minutes=settings.BOOKING_CLEANUP_INTERVAL_MINUTES)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        instance = self.instance
        starting_at = data.get('starting_at', getattr(instance, 'starting_at', None))
        ending_at = data.get('ending_at', getattr(instance, 'ending_at', None))
        guest_count = data.get('guest_count', getattr(instance, 'guest_count', None))
        table = data.get('table', getattr(instance, 'table', None))

        if starting_at and ending_at:
            if starting_at >= ending_at:
                raise serializers.ValidationError({'ending_at': 'Дата окончания должна быть позже даты начала.'})
            if starting_at < timezone.now():
                raise serializers.ValidationError({'starting_at': 'Бронирование не может быть создано в прошлом.'})

        if guest_count and table:
            if guest_count <= 0:
                raise serializers.ValidationError({'guest_count': 'Количество гостей должно быть больше 0.'})
            if guest_count > table.seats:
                raise serializers.ValidationError({'guest_count': 'Количество гостей не может превышать количество мест за столом.'})

        if table and starting_at and ending_at:
            overlap = Booking.objects.filter(
                table=table,
                starting_at__lt=ending_at + CLEANUP_INTERVAL,
                ending_at__gt=starting_at - CLEANUP_INTERVAL,
            ).exclude(status='cancelled')

            if instance:
                overlap = overlap.exclude(pk=instance.pk)

            if overlap.exists():
                raise serializers.ValidationError(
                    {'table': 'Этот стол уже забронирован на выбранное время (15 мин на уборку).'}
                )

        return data