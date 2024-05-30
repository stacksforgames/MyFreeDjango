# Generated by Django 3.2.9 on 2024-02-01 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0074_auto_20240129_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='comment',
            field=models.TextField(default='', verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='contract',
            name='revoked',
            field=models.BooleanField(default=False, verbose_name='Контракт аннулирован'),
        ),
    ]