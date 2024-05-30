# Generated by Django 3.2.9 on 2023-07-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0066_auto_20230701_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='agencyphone',
            field=models.TextField(default='', verbose_name='Телефон агентства'),
        ),
        migrations.AddField(
            model_name='contract',
            name='clientphone',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Телефон клиента'),
        ),
    ]
