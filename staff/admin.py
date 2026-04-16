from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone', 'created_at')
    list_filter = ('role',)
    search_fields = ('name', 'phone')