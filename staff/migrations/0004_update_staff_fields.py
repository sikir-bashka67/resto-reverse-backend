from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_staff_name_alter_staff_phone_alter_staff_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Staff name'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='role',
            field=models.CharField(max_length=100, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='phone',
            field=models.CharField(max_length=16, unique=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
    ]
