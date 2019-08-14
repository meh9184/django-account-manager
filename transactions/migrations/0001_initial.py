# Generated by Django 2.2.4 on 2019-08-15 02:45

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(max_length=20)),
                ('account_bank', models.CharField(choices=[('토스', '토스'), ('농협', '농협'), ('하나', '하나은행'), ('신한', '신한은행'), ('국민', '국민은행'), ('우리', '우리은행')], max_length=10)),
                ('user_name', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('10'))])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no_to', models.CharField(max_length=20)),
                ('account_no_from', models.CharField(max_length=20)),
                ('account_bank_to', models.CharField(choices=[('토스', '토스'), ('농협', '농협'), ('하나', '하나은행'), ('신한', '신한은행'), ('국민', '국민은행'), ('우리', '우리은행')], max_length=10)),
                ('account_bank_from', models.CharField(choices=[('토스', '토스'), ('농협', '농협'), ('하나', '하나은행'), ('신한', '신한은행'), ('국민', '국민은행'), ('우리', '우리은행')], max_length=10)),
                ('receiver_id', models.IntegerField()),
                ('receiver_name', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('10'))])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(max_length=20)),
                ('account_bank', models.CharField(choices=[('토스', '토스'), ('농협', '농협'), ('하나', '하나은행'), ('신한', '신한은행'), ('국민', '국민은행'), ('우리', '우리은행')], max_length=10)),
                ('user_name', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=0, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('10'))])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
