# Generated by Django 3.2.9 on 2023-06-29 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0064_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='turnover',
            name='bid',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.bid'),
        ),
    ]