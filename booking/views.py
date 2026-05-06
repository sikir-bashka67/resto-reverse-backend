from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer
from rest_framework import serializers


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user.client)

    def perform_create(self, serializer):
        try:
            client = self.request.user.client
        except AttributeError:
            from clients.models import Client
            client = Client.objects.filter(user=self.request.user).first()

        if not client:
            raise serializers.ValidationError("Этот аккаунт не привязан к профилю клиента.")
        serializer.save(client=client)