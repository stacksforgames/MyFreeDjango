# Generated by Django 3.2.9 on 2022-12-10 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0045_archivedetail_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='history',
            field=models.TextField(blank=True, default='', null=True, verbose_name='История изменений'),
        ),
    ]
