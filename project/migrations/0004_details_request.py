# Generated by Django 3.2.9 on 2021-11-17 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_details_goods'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.request'),
            preserve_default=False,
        ),
    ]