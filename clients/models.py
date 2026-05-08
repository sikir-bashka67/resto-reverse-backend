from django.core.exceptions import ValidationError
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя клиента')
    phone = models.CharField(max_length=16, verbose_name='Телефон', unique=True)
    password = models.CharField(max_length=128, verbose_name='Пароль')
    email = models.EmailField(verbose_name='E-mail')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} - {self.phone}'

    def clean(self):
        self.name = (self.name or '').strip()
        self.phone = (self.phone or '').strip()

        if not self.name:
            raise ValidationError('Имя клиента не может быть пустым.')

        normalized_phone = self.phone.lstrip('+')
        if not normalized_phone.isdigit():
            raise ValidationError("Телефон должен содержать только цифры и может начинаться с '+'.")

        if not 9 <= len(normalized_phone) <= 15:
            raise ValidationError('Длина телефона должна быть от 9 до 15 цифр.')

        if len(self.password or '') < 8:
            raise ValidationError('Пароль должен содержать не менее 8 символов.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
