from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


class Staff(AbstractUser):
    name = models.CharField(max_length=255, verbose_name="ФИО сотрудника", blank=True, null=False, unique=False)
    role = models.CharField(max_length=100, verbose_name="Должность")
    phone = models.CharField(max_length=14, verbose_name="Телефон", unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.name} - {self.role}"

    def clean(self):
        if not self.phone.isdigit():
            raise ValidationError("Телефон должен состоять только из цифр.")

        if len(self.phone) < 12:
            raise ValidationError("Слишком короткий номер телефона.")

        if not self.name or not self.name.strip():
            raise ValidationError("Имя не может быть пустым.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)