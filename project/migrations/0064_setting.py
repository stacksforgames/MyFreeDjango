# Generated by Django 3.2.9 on 2023-06-29 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0063_turnover'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', verbose_name='Описание')),
                ('type', models.IntegerField(choices=[(1, 'int'), (2, 'string'), (3, 'boolean'), (4, 'date')], default=1, verbose_name='Тип значения')),
                ('value', models.TextField(default='', verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]