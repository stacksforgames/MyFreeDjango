# Generated by Django 3.2.9 on 2023-10-27 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0072_bid_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='downtime',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Количество часов простоя'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='downtimecost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Стоимость часа простоя'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='pumptransfer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Переезд автобетононасоса'),
        ),
    ]
