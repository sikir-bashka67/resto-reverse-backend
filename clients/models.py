from django.db import models
from django.core.exceptions import ValidationError
from common.validators import validate_phone


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО клиента", unique=True, blank=False, null=False)
    phone = models.CharField(max_length=15, verbose_name="Телефон", unique=True, blank=False, null=False, validators=[validate_phone])
    password = models.CharField(max_length=128, verbose_name="Пароль")
    email = models.EmailField(verbose_name="E-mail")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.name} - {self.phone}"

    def clean(self):
        if len(self.phone) < 15:
            raise ValidationError("Слишком короткий номер телефона.")

        if not self.name or not self.name.strip():
            raise ValidationError("Имя не может быть пустым.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)