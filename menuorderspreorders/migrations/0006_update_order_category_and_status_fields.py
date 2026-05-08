import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuorderspreorders', '0005_alter_order_user_alter_preorder_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Menu item name'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('requested', 'Requested'),
                    ('processing', 'Processing'),
                    ('was_given', 'Was given'),
                ],
                default='processing',
                max_length=50,
                verbose_name='Order status',
            ),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='status',
            field=models.CharField(
                choices=[
                    ('requested', 'Requested'),
                    ('processing', 'Processing'),
                    ('was_given', 'Was given'),
                ],
                default='processing',
                max_length=50,
                verbose_name='Preorder status',
            ),
        ),
        migrations.AlterField(
            model_name='preorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=30, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birth date'),
        ),
        migrations.AlterField(
            model_name='preorderitem',
            name='price_at_ordering_time',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price at ordering time'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price_at_ordering_time',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price at ordering time'),
        ),
    ]
