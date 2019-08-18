#!/usr/bin/env python
from django.core.management.base import BaseCommand 
from users.models import Account 

import time, datetime, threading


def setInterval(func, time):
    e = threading.Event()

    while not e.wait(time):
        print('CRON JOB has run at', datetime.datetime.now().strftime('%H:%M'), '!')
        func()


def print_results(data):
    dash = '-' * 95

    print(dash)

    for i in range(len(data)):
        print('%-4s%-10s%-19s%-8s%-6s%-6s%-14s%-16s%s'%(
            data[i][0],     # NO
            data[i][1],     # RESULT
            data[i][2],     # USER
            data[i][3],     # NAME
            data[i][4],     # TYPE
            data[i][5],     # BANK
            data[i][6],     # ACCOUNT NO
            data[i][7],     # WITHD_AMNT_LMT
            data[i][8]      # TRANS_NO_LMT
        ))
        if i==0:
            print(dash)
    print(dash+'\n')


def reset_limits():
    accounts = Account.objects.all()

    data = [[
        'NO',
        'RESULT',
        'USER',
        'NAME',
        'TYPE',
        'BANK',
        'ACCOUNT NO',
        'WITHD_AMNT_LMT',
        'TRANS_NO_LMT'
    ]]

    for i, account in enumerate(accounts):
        if account.account_type == '일반':
            account.limit_once = 300000
            account.limit_daily = 300000

        elif account.account_type == '급여':
            account.limit_once = 10000000
            account.limit_daily = 100000000

        elif account.account_type == '적금':
            account.limit_once = 0
            account.limit_daily = 0

        account.daily_transfer_number = 3
        account.save()

        data.append([
            str(i+1),
            'COMPLETE',
            account.user.email,
            account.user.full_name,
            account.account_type,
            account.bank,
            account.account_no,
            account.limit_daily,
            account.daily_transfer_number
        ])

    print_results(data)


class Command(BaseCommand):
    help = 'Reset Limits'


    def add_arguments(self, parser):
        parser.add_argument('type', type=str)
        parser.add_argument('time', type=int)


    def handle(self, *args, **options):
        reset_type = options['type']
        reset_time = options['time']

        total_wait_to_second = 0

        if reset_type == 'cron':
            now = datetime.datetime.now()

            now_hour = int(now.strftime('%H'))
            now_minute = int(now.strftime('%M'))

            wait_hour =  reset_time - now_hour
            wait_minute = (60 - now_minute) % 60

            total_wait_to_second = (wait_hour * 60 * 60) + (wait_minute * 60)

        elif reset_type == 'interval':
            total_wait_to_second = (reset_time * 60)

        else:
            return

        setInterval(reset_limits, total_wait_to_second)
