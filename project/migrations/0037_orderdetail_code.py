# Generated by Django 3.2.9 on 2022-06-14 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_orderdetail_sample_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='code',
            field=models.TextField(blank=True, default='', verbose_name='Код'),
        ),
    ]
