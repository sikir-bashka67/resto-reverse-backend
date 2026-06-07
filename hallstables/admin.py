from django.contrib import admin
from .models import Hall, Table

class TableInline(admin.TabularInline):
    model = Table
    extra = 1

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity_info']
    inlines = [TableInline]

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    search_fields = ['name', 'table_number']
    list_display = ['name', 'table_number', 'hall', 'seats', 'status']