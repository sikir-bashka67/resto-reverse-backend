from django.db import models
from rest_framework.exceptions import ValidationError
from hallstables.models import Table
from clients.models import Client
from django.utils import timezone


class Booking(models.Model):
    STATUS_CHOICES = [('created', 'Created'), ('confirmed', 'Confirmed'), ('guest_arrived', 'Guest Arrived'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings', verbose_name="Клиент", unique=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings', verbose_name="Стол")
    starting_at = models.DateTimeField(verbose_name="Время начала")
    ending_at = models.DateTimeField(verbose_name="Время окончания")
    guest_count = models.IntegerField(verbose_name="Количество гостей")
    status = models.CharField(max_length=50, verbose_name="Состояние")
    qr_code = models.CharField(max_length=255, verbose_name="QR-код")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['starting_at']

    def __str__(self):
        date_str = self.starting_at.strftime('%d.%m %H:%M')
        return f"Бронь: {self.client.name} | Стол: {self.table.name} | {date_str} | Статус: {self.status}"

    def clean(self):
        if self.guest_count <= 0 or Table.seats:
            raise ValidationError("Некорректные данные.")

        if self.starting_at <= self.ending_at:
            raise ValidationError("Нелогичное выражение.")

        if self.starting_at < timezone.now():
            raise ValidationError("Невозможна бронь в прошлом.")

        overlap = Booking.objects.filter(starting_at__lt=self.ending_at, table=self.table, ending_at__gt=self.starting_at).exclude(pk=self.pk)

        if overlap.exists():
            raise ValidationError("На это время уже есть бронь.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)