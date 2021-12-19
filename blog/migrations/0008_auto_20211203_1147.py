# Generated by Django 3.2.8 on 2021-12-03 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20211203_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleHit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article')),
                ('ip_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.ipaddress')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='hits',
            field=models.ManyToManyField(blank=True, through='blog.ArticleHit', to='blog.IpAddress', verbose_name='بازدید ها '),
        ),
    ]