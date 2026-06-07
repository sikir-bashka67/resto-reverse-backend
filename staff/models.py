from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Staff(AbstractUser):
    name = models.CharField(max_length=255, verbose_name='Имя сотрудника', blank=True, null=False)
    role = models.CharField(max_length=100, verbose_name='Должность')
    phone = models.CharField(max_length=16, verbose_name='Телефон', unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.name} - {self.role}'

    def clean(self):
        self.name = (self.name or '').strip()
        self.phone = (self.phone or '').strip()

        if self.phone:
            normalized_phone = self.phone.lstrip('+')
            if not normalized_phone.isdigit():
                raise ValidationError({'phone': "Телефон должен содержать только цифры и может начинаться с '+'."})
            if not 9 <= len(normalized_phone) <= 15:
                raise ValidationError({'phone': 'Длина телефона должна быть от 9 до 15 цифр.'})
        if not self.name:
            raise ValidationError({'name': 'Имя сотрудника не может быть пустым.'})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)