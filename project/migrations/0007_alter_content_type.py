# Generated by Django 3.2.9 on 2021-11-30 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_house_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('a', 'Материалы'), ('b', 'Работа'), ('c', 'Техника'), ('d', 'Доставка')], max_length=1),
        ),
    ]
