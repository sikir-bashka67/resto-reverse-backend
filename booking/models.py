from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from clients.models import Client
from hallstables.models import Table


class Booking(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('confirmed', 'Confirmed'),
        ('guest_arrived', 'Guest Arrived'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings', verbose_name='Клиент')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings', verbose_name='Стол')
    starting_at = models.DateTimeField(verbose_name='Время начала')
    ending_at = models.DateTimeField(verbose_name='Время окончания')
    guest_count = models.IntegerField(verbose_name='Количество гостей')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    qr_code = models.CharField(max_length=255, blank=True, verbose_name='QR-код')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['starting_at']

    def __str__(self):
        date_str = self.starting_at.strftime('%d.%m %H:%M')
        return f'Бронь: {self.client.name} | Стол: {self.table.name} | {date_str} | Статус: {self.status}'

    def clean(self):
        if self.guest_count <= 0:
            raise ValidationError({'guest_count': 'Количество гостей должно быть больше 0.'})

        if self.table and self.guest_count > self.table.seats:
            raise ValidationError({'table' and 'guest_count': f'Этот стол вмещает только {self.table.seats} гостей.'})

        if self.starting_at >= self.ending_at:
            raise ValidationError({'starting_at' and 'ending_at': 'Время начала должно быть раньше времени окончания.'})

        if self.starting_at < timezone.now():
            raise ValidationError({'starting_at': 'Нельзя создать бронирование в прошлом.'})

        overlap = Booking.objects.filter(
            table=self.table,
            starting_at__lt=self.ending_at,
            ending_at__gt=self.starting_at,
        ).exclude(pk=self.pk)

        if overlap.exists():
            raise ValidationError({'booking': 'Этот стол уже забронирован на выбранное время.'})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)