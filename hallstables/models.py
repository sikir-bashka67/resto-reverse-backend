from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from rest_framework.exceptions import ValidationError


class Hall(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название зала", unique=True)
    width = models.FloatField(verbose_name="Ширина")
    height = models.FloatField(verbose_name="Высота")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"

    def __str__(self):
        return f"Зал: {self.name} ({self.height} x {self.width} метров)"

    def clean(self):
        if self.width <= 0 or self.height <= 0:
            raise ValidationError("Значение этой строки не может равняться нулю.")

        if " " in self.name:
            raise ValidationError("Эта строка не может содержать пробелы.")

        if not self.name.strip():
            raise ValidationError("Эта строка не может быть пустой.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def capacity_info(self):
        tables = self.tables.all()
        total = sum(table.seats for table in tables)
        return f"Мест: {total} (Столов: {tables.count()})"

    capacity_info.short_description = 'Вместимость'


class Table(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('occupied', 'Occupied'), ('reserved', 'Reserved'), ('out_of_service', 'Out_of_service')]
    table_number = models.IntegerField(unique=True, null=False, blank=False)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='tables', verbose_name="Зал")
    name = models.CharField(max_length=255, verbose_name="Название стола", unique=True, blank=False, null=False)
    seats = models.PositiveIntegerField(verbose_name="Места")
    type = models.CharField(max_length=50, verbose_name="Тип")
    x = models.FloatField(verbose_name="Координата X")
    y = models.FloatField(verbose_name="Координата Y")
    status = models.CharField(verbose_name="Состояние", null=False, blank=False, max_length=20)
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        unique_together = ('hall', 'name')

    def clean(self):
        if " " in self.name:
            raise ValidationError("Эта строка не может содержать пробелы.")

        if self.seats <= 0:
            raise ValidationError("Эта строка обязательно должна быть положительной.")

        if self.x > self.hall.x or self.y > self.hall.y or self.x < 0 or self.y < 0:
            raise ValidationError("Это значение не может быть выше установленного значения зала.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        is_new = self.pk is None

        if is_new:
            super().save(*args, **kwargs)
        qr_data = f"https://resto-fresh.com/table/{self.pk}/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')

        filename = f'table_qr_{self.pk}.png'

        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)
        # Сделал ИИ-шкой, так как, ну, банально, мы такое не проходили, но структуру кода понимаю!

    def __str__(self):
        return f"Стол {self.name} | {self.hall.name} | Мест: {self.seats} | Тип: {self.type}"