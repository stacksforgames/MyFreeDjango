# Generated by Django 3.2.9 on 2023-04-30 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0049_bid_supervisor'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название кассы')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('hidden', models.BooleanField(default=False, verbose_name='Скрыто')),
            ],
            options={
                'verbose_name': 'Касса',
                'verbose_name_plural': 'Кассы',
            },
        ),
        migrations.CreateModel(
            name='SubCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название локальной кассы')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('date', models.DateTimeField(verbose_name='Остаток на дату')),
                ('closedate', models.DateTimeField(verbose_name='Дата закрытия')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('hidden', models.BooleanField(default=False, verbose_name='Скрыто')),
                ('cashregister', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.cashregister')),
            ],
            options={
                'verbose_name': 'Локальная касса',
                'verbose_name_plural': 'Локальнаые кассы',
            },
        ),
    ]