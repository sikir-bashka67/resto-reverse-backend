from django.contrib import admin
from .models import Menu, Order, OrderItem, PreOrder, PreOrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('menu_item', 'quantity', 'price_at_order_time')

class PreOrderItemInline(admin.TabularInline):
    model = PreOrderItem
    extra = 1
    fields = ('menu_item', 'quantity', 'price_at_order_time')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'created_at')
    list_filter = ('is_available',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id_short', 'table', 'status', 'created_at')
    list_filter = ('status', 'table__hall')
    inlines = [OrderItemInline]

    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = 'ID'

@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ('booking', 'created_at')
    inlines = [PreOrderItemInline]