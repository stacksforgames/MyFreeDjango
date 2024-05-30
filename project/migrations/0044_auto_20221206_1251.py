# Generated by Django 3.2.9 on 2022-12-06 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0043_estimate_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='phase',
            name='comment',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='phase',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
        migrations.AddField(
            model_name='phase',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Скрыто'),
        ),
    ]