from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО клиента")
    phone = models.CharField(max_length=14, verbose_name="Телефон", unique=True)
    email = models.EmailField(verbose_name="E-mail")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.name} - {self.phone}"