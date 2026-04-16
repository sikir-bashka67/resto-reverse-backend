from django.contrib import admin
from .models import Hall, Table

class TableInline(admin.TabularInline):
    model = Table
    extra = 1

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity_info']
    inlines = [TableInline]

admin.site.register(Table)