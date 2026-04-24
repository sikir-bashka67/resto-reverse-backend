from django.db import models
from django.conf import settings


class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название блюда")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Меню"

    def __str__(self):
        status = "Y" if self.is_available else "N"
        return f"{status} {self.name} ({self.price} с)"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    class Meta:
        verbose_name = "Категория блюд"
        verbose_name_plural = "Категории блюд"

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    location = models.CharField(max_length=30, blank=True, verbose_name="Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    def __str__(self):
        return f"Профиль пользователя: {self.user.username}"


class PreOrder(models.Model):
    booking = models.ForeignKey('booking.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        booking_id = self.booking.id if self.booking else "Без брони"
        return f"Предзаказ №{self.pk} (Бронь: {booking_id})"


class Order(models.Model):
    booking = models.ForeignKey('booking.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey('hallstables.Table', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ №{str(self.pk)[:8]} | Стол {self.table.name} | {self.status}"


class PreOrderItem(models.Model):
    preorder = models.ForeignKey(PreOrder, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    price_at_order_time = models.DecimalField(max_digits=10,decimal_places=2 , verbose_name="Цена при заказе")

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity} (по {self.price_at_order_time} с)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена при заказе")

    def __str__(self):
        return f"{self.menu_item.name} ({self.quantity} шт.)"