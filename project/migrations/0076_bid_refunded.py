# Generated by Django 3.2.9 on 2024-04-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0075_auto_20240201_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='refunded',
            field=models.BooleanField(default=False, verbose_name='Возвращена'),
        ),
    ]