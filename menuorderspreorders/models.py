from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название блюда', unique=True)
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Меню'

    def __str__(self):
        status = 'Y' if self.is_available else 'N'
        return f'{status} {self.name} ({self.price})'

    def clean(self):
        self.name = (self.name or '').strip()
        if not self.name:
            raise ValidationError('Название блюда не может быть пустым.')
        if self.price <= 0:
            raise ValidationError('Цена должна быть больше 0.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория', unique=True)

    class Meta:
        verbose_name = 'Категория меню'
        verbose_name_plural = 'Категории меню'

    def __str__(self):
        return self.name

    def clean(self):
        self.name = (self.name or '').strip()
        if not self.name:
            raise ValidationError('Название категории не может быть пустым.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', unique=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    location = models.CharField(max_length=30, blank=True, verbose_name='Город')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def __str__(self):
        return f'Профиль: {self.user.username}'

    def clean(self):
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError('Дата рождения не может быть в будущем.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PreOrder(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processing', 'Processing'),
        ('was_given', 'Was given'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='processing', verbose_name='Статус предзаказа')
    booking = models.ForeignKey('booking.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        booking_id = self.booking.id if self.booking else 'Без брони'
        return f'Предзаказ #{self.pk} (Бронь: {booking_id})'


class Order(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processing', 'Processing'),
        ('was_given', 'Was given'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey('booking.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey('hallstables.Table', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='processing', verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.pk} | Стол {self.table.name} | {self.status}'


class PreOrderItem(models.Model):
    preorder = models.ForeignKey(PreOrder, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')
    price_at_ordering_time = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена на момент заказа')

    def __str__(self):
        return f'{self.menu_item.name} x {self.quantity} ({self.price_at_ordering_time})'

    def clean(self):
        if self.price_at_ordering_time <= 0:
            raise ValidationError('Цена на момент заказа должна быть больше 0.')
        if self.quantity <= 0:
            raise ValidationError('Количество должно быть больше 0.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')
    price_at_ordering_time = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена на момент заказа')

    def __str__(self):
        return f'{self.menu_item.name} ({self.quantity})'

    def clean(self):
        if self.price_at_ordering_time <= 0:
            raise ValidationError('Цена на момент заказа должна быть больше 0.')
        if self.quantity <= 0:
            raise ValidationError('Количество должно быть больше 0.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)