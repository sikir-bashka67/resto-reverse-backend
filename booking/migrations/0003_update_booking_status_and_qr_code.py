from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(
                choices=[
                    ('created', 'Created'),
                    ('confirmed', 'Confirmed'),
                    ('guest_arrived', 'Guest Arrived'),
                    ('completed', 'Completed'),
                    ('cancelled', 'Cancelled'),
                ],
                default='created',
                max_length=50,
                verbose_name='Status',
            ),
        ),
        migrations.AlterField(
            model_name='booking',
            name='qr_code',
            field=models.CharField(blank=True, max_length=255, verbose_name='QR code'),
        ),
    ]
