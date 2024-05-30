# Generated by Django 3.2.9 on 2022-12-06 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0044_auto_20221206_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivedetail',
            name='type',
            field=models.CharField(choices=[('a', 'Материалы'), ('b', 'Работа'), ('c', 'Техника'), ('d', 'Доставка'), ('e', 'Перемещение'), ('f', 'Прочие расходы')], default='f', max_length=1),
        ),
    ]
