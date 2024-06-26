# Generated by Django 3.2.9 on 2023-05-06 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0054_auto_20230430_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Earning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Пояснения')),
                ('date', models.DateTimeField(verbose_name='Дата')),
                ('locked', models.BooleanField(default=False, verbose_name='Заблокировано')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('credit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_account', to='project.account')),
                ('expense_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_account', to='project.account')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.object')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subcash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.subcash')),
            ],
            options={
                'verbose_name': 'Доход',
                'verbose_name_plural': 'Доходы',
            },
        ),
    ]
