from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


class Hall(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название зала")
    width = models.FloatField(verbose_name="Ширина")
    height = models.FloatField(verbose_name="Высота")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"

    def __str__(self):
        return f"Зал: {self.name} ({self.height} x {self.width} метров)"

    def capacity_info(self):
        tables = self.tables.all()
        total = sum(table.capacity for table in tables)
        return f"Мест: {total} (Столов: {tables.count()})"

    capacity_info.short_description = 'Вместимость'


class Table(models.Model):
    table_number = models.IntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='tables', verbose_name="Зал")
    name = models.CharField(max_length=255, verbose_name="Название стола")
    seats = models.PositiveIntegerField(verbose_name="Места")
    type = models.CharField(max_length=50, verbose_name="Тип")
    x = models.FloatField(verbose_name="Координата X")
    y = models.FloatField(verbose_name="Координата Y")
    status = models.CharField(max_length=50, verbose_name="Статус")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        unique_together = ('hall', 'name')

    def save(self, *args, **kwargs):
        qr_data = f"https://resto.com/table/{self.pk}/"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'table_qr_{self.table_number}.png'
        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)
        # Сделал ИИ-шкой, так как, ну, банально, мы такое не проходили, но структуру кода понимаю!

    def __str__(self):
        return f"Стол {self.name} | {self.hall.name} | Мест: {self.seats} | Тип: {self.type}"