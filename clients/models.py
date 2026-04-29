from django.db import models
from rest_framework.exceptions import ValidationError


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО клиента", unique=True, blank=False, null=False)
    phone = models.IntegerField(max_length=12, verbose_name="Телефон", unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, verbose_name="Пароль")
    email = models.EmailField(verbose_name="E-mail")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.name} - {self.phone}"

    def clean(self):
        if " " in self.phone or self.name:
            raise ValidationError("Эта строка не может содержать пробелы.")

        if self.phone != int:
            raise ValidationError("Это числовое поле.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)