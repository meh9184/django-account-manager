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
        related_name='Deposit',
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
    action_name = 'Deposit'

    def get_action_name(self):
        return self.action_name 

    def set_action_name(self, action_name):
        self.action_name = action_name
        return action_name

    def __str__(self):
        return str(self.id)

class Withdraw(models.Model):
    account = models.ForeignKey(
        Account,
        related_name='Withdraw',
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
    action_name = 'Withdraw'

    def get_action_name(self):
        return self.action_name 

    def set_action_name(self, action_name):
        self.action_name = action_name
        return action_name

    def __str__(self):
        return str(self.id)


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
    action_name = 'Transfer'

    def get_action_name(self):
        return self.action_name 

    def set_action_name(self, action_name):
        self.action_name = action_name
        return action_name

    def __str__(self):
        return str(self.id)