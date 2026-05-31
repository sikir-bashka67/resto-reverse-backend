from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
        search_fields = ['name', 'phone', 'email']
        list_display = ['name', 'phone']