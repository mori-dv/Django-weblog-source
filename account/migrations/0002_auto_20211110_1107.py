# Generated by Django 3.2.8 on 2021-11-10 07:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_author',
            field=models.BooleanField(default=False, verbose_name='وضعیت\u200c نویسندگی'),
        ),
        migrations.AddField(
            model_name='user',
            name='vip_user',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='مدت زمان کاربر ویژه'),
        ),
    ]
