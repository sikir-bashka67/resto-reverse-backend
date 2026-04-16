from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Staff(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="ФИО сотрудника")
    role = models.CharField(max_length=255, verbose_name="Должность")
    phone = models.CharField(max_length=14, verbose_name="Телефон", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.name} - {self.role}"