from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(unique=True)
    full_name       = models.CharField(max_length=20)
    mobile_no       = models.IntegerField(blank=False)
    date_joined     = models.DateTimeField(default=timezone.now)
    balance         = models.IntegerField(default=0)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    main_account_no = models.CharField(max_length=20)
    account_number  = models.IntegerField(default=0)

    location = (
        ('S', '서울'),
        ('I', '인천'),
        ('K', '경기'),
    )
    loc = models.CharField(max_length=1, choices=location)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Account(models.Model):
    account_no              = models.CharField(max_length=20)
    user                    = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance                 = models.IntegerField(default=0)
    daily_transfer_number   = models.IntegerField(default=3)
    is_main_account         = models.BooleanField(default=False)

    bank_list = (
        ('토스', '토스'),
        ('농협', '농협'),
        ('하나', '하나은행'),
        ('신한', '신한은행'),
        ('국민', '국민은행'),
        ('우리', '우리은행'),
    )
    bank = models.CharField(max_length=10, choices=bank_list)

    account_type_list = (
        ('일반', '일반'),
        ('급여', '급여'),
        ('적금', '적금'),
    )
    account_type = models.CharField(max_length=10, choices=account_type_list)

    def _get_limit_once(self):
        if self.account_type == '일반':
            return 300000
        elif self.account_type == '급여':
            return 10000000
        elif self.account_type == '적금':
            return 0
    limit_once = property(_get_limit_once)
    
    def _get_limit_daily(self):
        if self.account_type == '일반':
            return 300000
        elif self.account_type == '급여':
            return 100000000
        elif self.account_type == '적금':
            return 0
    limit_daily = property(_get_limit_daily)


    # def clean(self):
    #     """
    #     Throw ValidationError if you try to save more than one model instance
    #     See: http://stackoverflow.com/a/6436008
    #     """
    #     model = self.__class__
    #     if (model.objects.count() > 5 and
    #             self.id != model.objects.get().id):
    #         raise ValidationError(
    #             "Can only create 5 instance of %s." % model.__name__)