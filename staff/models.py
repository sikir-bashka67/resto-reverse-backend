from django.contrib.auth.models import AbstractUser
from django.db import models


class Staff(AbstractUser):
    name = models.CharField(max_length=255, verbose_name="ФИО сотрудника", blank=True, null=True)
    role = models.CharField(max_length=255, verbose_name="Должность")
    phone = models.CharField(max_length=14, verbose_name="Телефон", unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.name} - {self.role}"