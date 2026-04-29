from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


class Staff(AbstractUser):
    name = models.CharField(max_length=255, verbose_name="ФИО сотрудника", blank=True, null=False, unique=False)
    role = models.CharField(max_length=100, verbose_name="Должность")
    phone = models.IntegerField(max_length=12, verbose_name="Телефон", unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.name} - {self.role}"

    def clean(self):
        if " " in self.phone or self.name:
            raise ValidationError("Эта строка не может содержать пробелы.")
        if self.phone != int:
            raise ValidationError("Это числовое поле.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)