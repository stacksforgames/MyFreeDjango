# Generated by Django 3.2.9 on 2023-05-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0056_auto_20230506_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='earning',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=12),
            preserve_default=False,
        ),
    ]
