# Generated by Django 3.2.9 on 2023-04-30 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0050_cashregister_subcash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcash',
            name='closedate',
            field=models.DateTimeField(null=True, verbose_name='Дата закрытия'),
        ),
    ]
