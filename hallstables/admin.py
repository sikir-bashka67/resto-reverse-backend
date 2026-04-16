from django.contrib import admin
from .models import Hall, Table

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'created_at')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'hall', 'seats', 'type', 'status', 'is_deleted')
    list_filter = ('hall', 'status', 'type')
    search_fields = ('name',)