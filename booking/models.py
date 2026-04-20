from django.db import models
from hallstables.models import Table
from clients.models import Client


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings', verbose_name="Клиент")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings', verbose_name="Стол")
    starting_at = models.DateTimeField(verbose_name="Время начала")
    ending_at = models.DateTimeField(verbose_name="Время окончания")
    guest_count = models.IntegerField(verbose_name="Количество гостей")
    status = models.CharField(max_length=50, verbose_name="Статус")
    qr_code = models.CharField(max_length=255, verbose_name="QR-код")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-starting_at']

    def __str__(self):
        date_str = self.starting_at.strftime('%d.%m %H:%M')
        return f"Бронь: {self.client.name} | Стол: {self.table.name} | {date_str} | Статус: {self.status}"