from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    name = models.CharField(max_length=100, verbose_name='Имя клиента')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Телефон должен быть в формате: '+999999999'. От 9 до 15 цифр.")
    phone = models.CharField(validators=[phone_regex], max_length=16, verbose_name='Телефон', unique=True)
    email = models.EmailField(verbose_name='E-mail')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.phone})'

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        if self.phone:
            self.phone = self.phone.strip()
        super().save(*args, **kwargs)