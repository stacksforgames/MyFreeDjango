# Generated by Django 3.2.9 on 2022-06-06 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0032_archivedetail_new_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='', verbose_name='Примечание')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('hidden', models.BooleanField(default=False, verbose_name='Скрыто')),
            ],
            options={
                'verbose_name': 'Шаблон заказа',
                'verbose_name_plural': 'Шаблоны заказа',
            },
        ),
        migrations.AlterField(
            model_name='delivery',
            name='concrete_grade',
            field=models.CharField(choices=[('a', '300'), ('b', '350'), ('c', '400')], max_length=1),
        ),
        migrations.CreateModel(
            name='SampleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(blank=True, default='', verbose_name='Код')),
                ('description', models.TextField(default='', verbose_name='Описание')),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('measure', models.CharField(choices=[('kg', 'кг'), ('kk', 'т.'), ('m1', 'м.'), ('m3', 'м3'), ('m2', 'кв.м'), ('pm', 'пог.м'), ('pc', 'шт.'), ('2p', 'пар.'), ('hh', 'час.'), ('lt', 'л.'), ('mt', 'мл.'), ('on', 'ед.'), ('ms', 'машина')], max_length=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.sample')),
            ],
            options={
                'verbose_name': 'Позиция шаблона заказа',
                'verbose_name_plural': 'Позиции шаблона заказа',
            },
        ),
    ]
