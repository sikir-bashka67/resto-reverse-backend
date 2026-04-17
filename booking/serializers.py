from rest_framework import serializers
from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'client', 'table', 'starting_at', 'ending_at', 'guest_count']