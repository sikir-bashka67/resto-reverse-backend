from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_booking_reminder(booking_id):
    from booking.models import Booking
    try:
        booking = Booking.objects.select_related('client', 'table').get(pk=booking_id)
    except Booking.DoesNotExist:
        return

    send_mail(
        subject='Напоминание о бронировании',
        message=f'Мы ждём вас сегодня в {booking.starting_at.strftime("%H:%M")}. Стол: {booking.table.name}.',
        from_email='noreply@resto-reserve.com',
        recipient_list=[booking.client.email],
        fail_silently=True,
    )