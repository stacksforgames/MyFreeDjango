# Generated by Django 3.2.9 on 2022-05-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0030_auto_20220427_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='type',
            field=models.CharField(default='0', max_length=1),
        ),
    ]