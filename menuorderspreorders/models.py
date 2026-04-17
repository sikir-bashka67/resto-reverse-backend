from django.db import models
import uuid


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, verbose_name="Название блюда")
    description = models.TextField(verbose_name="Описание")
    price = models.FloatField(verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True)

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


class PreOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('booking.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Предзаказ к брони {self.booking.id}"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('booking.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey('hallstables.Table', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ №{str(self.id)[:8]} | Стол {self.table.name} | {self.status}"


class PreOrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    preorder = models.ForeignKey(PreOrder, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    price_at_order_time = models.FloatField(verbose_name="Цена при заказе")

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity} (по {self.price_at_order_time} с)"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Количество")
    price_at_order_time = models.FloatField(verbose_name="Цена при заказе")

    def __str__(self):
        return f"{self.menu_item.name} ({self.quantity} шт.)"