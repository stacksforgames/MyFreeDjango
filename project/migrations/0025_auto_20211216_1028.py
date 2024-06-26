# Generated by Django 3.2.9 on 2021-12-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0024_alter_bid_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='highlighted',
            field=models.BooleanField(default=False, verbose_name='Помечено'),
        ),
        migrations.AlterField(
            model_name='content',
            name='measure',
            field=models.CharField(choices=[('kg', 'кг'), ('kk', 'т.'), ('m3', 'м3'), ('m2', 'кв.м'), ('pm', 'пг.м'), ('pc', 'шт.'), ('2p', 'пар.'), ('hh', 'час.'), ('lt', 'л.'), ('--', 'доставка')], max_length=2),
        ),
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('a', 'Материалы'), ('b', 'Работа'), ('c', 'Техника'), ('d', 'Доставка'), ('e', 'Перемещение')], max_length=1),
        ),
    ]
