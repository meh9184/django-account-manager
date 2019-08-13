from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from users.models import Account
from django.utils import timezone
    
from decimal import Decimal
User = settings.AUTH_USER_MODEL

class Deposit(models.Model):
    account = models.ForeignKey(
        Account,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    account_no = models.CharField(max_length=20)

    bank_list = (
        ('토스', '토스'),
        ('농협', '농협'),
        ('하나', '하나은행'),
        ('신한', '신한은행'),
        ('국민', '국민은행'),
        ('우리', '우리은행'),
    )
    account_bank = models.CharField(max_length=10, choices=bank_list)
    
    user_name = models.CharField(max_length=20)
    amount = models.DecimalField(
        decimal_places=0,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10'))
        ]
    )
    timestamp   = models.DateTimeField(auto_now_add=True)
    #timestamp = models.DateTimeField(blank=False,default=timezone.now)


    def __str__(self):
        return str(self.account.id)

class Withdraw(models.Model):
    account = models.ForeignKey(
        Account,
        related_name='withdraw',
        on_delete=models.CASCADE,
    )
    account_no = models.CharField(max_length=20)

    bank_list = (
        ('토스', '토스'),
        ('농협', '농협'),
        ('하나', '하나은행'),
        ('신한', '신한은행'),
        ('국민', '국민은행'),
        ('우리', '우리은행'),
    )
    account_bank = models.CharField(max_length=10, choices=bank_list)

    user_name = models.CharField(max_length=20)
    amount = models.DecimalField(
        decimal_places=0,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10'))
        ]
    )

    timestamp   = models.DateTimeField(auto_now_add=True)
    #timestamp = models.DateTimeField(blank=False,default=timezone.now)
    
    def __str__(self):
        return str(self.account.id)

class Transfer(models.Model):
    account = models.ForeignKey(
        Account,
        related_name='Transfer',
        on_delete=models.CASCADE,
    )
    account_no_to = models.CharField(max_length=20)
    account_no_from = models.CharField(max_length=20)

    bank_list = (
        ('토스', '토스'),
        ('농협', '농협'),
        ('하나', '하나은행'),
        ('신한', '신한은행'),
        ('국민', '국민은행'),
        ('우리', '우리은행'),
    )
    account_bank_to = models.CharField(max_length=10, choices=bank_list)
    account_bank_from = models.CharField(max_length=10, choices=bank_list)
    
    receiver_id = models.IntegerField()
    receiver_name = models.CharField(max_length=20)

    user_name = models.CharField(max_length=20)
    amount = models.DecimalField(
        decimal_places=0,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10'))
        ]
    )
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.id)
