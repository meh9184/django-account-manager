# Generated by Django 2.2.4 on 2019-08-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='limit_daily',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='limit_once',
            field=models.IntegerField(default=0),
        ),
    ]
