from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hallstables', '0002_alter_hall_name_alter_table_name_alter_table_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Hall name'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='width',
            field=models.FloatField(verbose_name='Width'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='height',
            field=models.FloatField(verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='table',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Table name'),
        ),
        migrations.AlterField(
            model_name='table',
            name='status',
            field=models.CharField(
                choices=[
                    ('available', 'Available'),
                    ('occupied', 'Occupied'),
                    ('reserved', 'Reserved'),
                    ('out_of_service', 'Out of service'),
                ],
                default='available',
                max_length=20,
                verbose_name='Status',
            ),
        ),
    ]
