# Generated by Django 3.2.9 on 2021-12-14 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_bid_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='number',
            field=models.IntegerField(default=0, verbose_name='Номер заявки'),
        ),
    ]
