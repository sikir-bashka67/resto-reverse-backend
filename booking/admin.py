from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id_short', 'client', 'table', 'starting_at', 'status', 'guest_count']
    list_filter = ['status', 'starting_at', 'table__hall']
    search_fields = ['client__name', 'client__phone', 'qr_code']
    list_editable = ['status', 'guest_count']
    date_hierarchy = 'starting_at'
    autocomplete_fields = ['client', 'table']

    def id_short(self, obj):
        return str(obj.id)[:8]
    id_short.short_description = 'ID'