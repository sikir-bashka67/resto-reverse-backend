from django.db import models
import uuid

class Hall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название зала")
    width = models.FloatField(verbose_name="Ширина")
    height = models.FloatField(verbose_name="Высота")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"

    def __str__(self):
        return f"Зал: {self.name} ({self.height} x {self.width} метров)"


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='tables', verbose_name="Зал")
    name = models.CharField(max_length=255, verbose_name="Название стола")
    seats = models.PositiveIntegerField(verbose_name="Места")
    type = models.CharField(max_length=50, verbose_name="Тип")
    x = models.FloatField(verbose_name="Координата X")
    y = models.FloatField(verbose_name="Координата Y")
    status = models.CharField(max_length=50, verbose_name="Статус")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        unique_together = ('hall', 'name')

    def __str__(self):
        return f"Стол {self.name} | {self.hall.name} | Мест: {self.seats} | Тип: {self.type}"