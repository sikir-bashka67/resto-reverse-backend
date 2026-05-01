from rest_framework import serializers
from booking.models import Booking
from django.utils import timezone


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        starting_at = data.get('starting_at') or (self.instance.starting_at if self.instance else None)
        ending_at = data.get('ending_at') or (self.instance.ending_at if self.instance else None)
        guest_count = data.get('guest_count') or (self.instance.guest_count if self.instance else None)
        table = data.get('table') or (self.instance.table if self.instance else None)

        if starting_at and ending_at:
            if starting_at >= ending_at:
                raise serializers.ValidationError("Дата окончания должна быть позже даты начала")
            if starting_at < timezone.now():
                raise serializers.ValidationError("Бронирование не может быть создано в прошлом")

        if guest_count and table:
            if guest_count <= 0:
                raise serializers.ValidationError("Количество гостей должно быть больше 0")
            if guest_count > table.seats:
                raise serializers.ValidationError("Количество гостей не может превышать количество мест за столом")

        if table and starting_at and ending_at:
            overlap = Booking.objects.filter(
                table=table,
                starting_at__lt=ending_at,
                ending_at__gt=starting_at
            )
            if self.instance:
                overlap = overlap.exclude(pk=self.instance.pk)
            if overlap.exists():
                raise serializers.ValidationError("Этот стол уже забронирован на выбранное время")

        return data