from io import BytesIO
import qrcode
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название зала', unique=True)
    width = models.FloatField(verbose_name='Ширина')
    height = models.FloatField(verbose_name='Высота')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        return f'Зал: {self.name} ({self.height} x {self.width} м)'

    def clean(self):
        self.name = (self.name or '').strip()
        if self.width <= 0 or self.height <= 0:
            raise ValidationError({'width' and 'height': 'Размеры зала должны быть больше 0.'})
        if not self.name:
            raise ValidationError({'name': 'Название зала не может быть пустым.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def capacity_info(self):
        tables = self.tables.all()
        total = sum(table.seats for table in tables)
        return f'Мест: {total} (Столов: {tables.count()})'

    capacity_info.short_description = 'Вместимость'


class Table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('out_of_service', 'Out of service'),
    ]

    table_number = models.IntegerField(unique=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='tables', verbose_name='Зал')
    name = models.CharField(max_length=255, verbose_name='Название стола')
    seats = models.PositiveIntegerField(verbose_name='Количество мест')
    type = models.CharField(max_length=50, verbose_name='Тип')
    x = models.FloatField(verbose_name='Координата X')
    y = models.FloatField(verbose_name='Координата Y')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='Статус')
    is_deleted = models.BooleanField(default=False, verbose_name='Удален')
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        unique_together = ('hall', 'name')

    def clean(self):
        self.name = (self.name or '').strip()

        if not self.name:
            raise ValidationError({'name': 'Название стола не может быть пустым.'})
        if self.seats <= 0:
            raise ValidationError({'seats': 'Количество мест должно быть больше 0.'})
        if self.x < 0 or self.y < 0 or self.x > self.hall.width or self.y > self.hall.height:
            raise ValidationError({'x' and 'y': 'Координаты стола должны находиться в пределах зала.'})

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # один save

        if is_new and not self.qr_code:
            self._generate_qr()

    def _generate_qr(self):
        qr_data = f'https://resto-fresh.com/table/{self.pk}/'
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format='PNG')

        self.qr_code.save(f'table_qr_{self.pk}.png', File(buffer), save=False)
        super().save(update_fields=['qr_code'])

    def __str__(self):
        return f'Стол {self.name} | {self.hall.name} | Мест: {self.seats} | Тип: {self.type}'