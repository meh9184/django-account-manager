#!/usr/bin/env python
from django.core.management.base import BaseCommand 
import argparse

from users.models import Account 
import datetime, time, re, threading


def set_interval(func, delay_time, reset_type):
    e = threading.Event()

    print('Current DATETIME is', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    print('Wating for next CRON JOB...')

    # 만약 cron 타입이라면
    if reset_type == 'cron':


        # 일단 time 만큼 기다린 후 프로세스 한번 수행하고
        
        time.sleep(delay_time)
        print('\nCRON JOB has run at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '!')
        func()
        print('\n\nCurrent DATETIME is', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        print('Wating for next CRON JOB...')
        
        # 하루 (60 * 60 * 24 초) 만큼의 delay로 set_interval 수행
        while not e.wait(60*60*24):
            print('\nCRON JOB has run at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '!')
            func()
            print('\n\nCurrent DATETIME is', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            print('Wating for next CRON JOB...')

    # 만약 interval 타입이라면
    elif reset_type == 'interval':
        # 매개변수로 넘어온 time 만큼의 delay로 set_interval 수행
        while not e.wait(delay_time):
            print('\nCRON JOB has run at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '!')
            func()
            print('\n\nCurrent DATETIME is', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            print('Wating for next CRON JOB...')

    else:
        return


def print_results(data):
    dash = '-' * 95

    for i in range(len(data)):
        if i==0:
            print(dash)
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
            print(dash)
        else:
            print('%-4s%-10s%-19s%-5s%-4s%-4s%-14s%-16s%s'%(
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
    print(dash)
    print(len(data)-1, 'ROW(S) HAVE BEEN UPDATED !')


def reset_limits():
    # 전체 Account객체를 select
    accounts = Account.objects.all()

    # 결과 출력을 위한 데이터 셋팅
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

    # 각 Acount 객체 마다 limit_daily와 daily_transfer_number를 리셋하고 저장
    for i, account in enumerate(accounts):
        if account.account_type == '일반':
            account.limit_daily = 300000

        elif account.account_type == '급여':
            account.limit_daily = 100000000

        elif account.account_type == '적금':
            account.limit_daily = 0

        account.daily_transfer_number = 3
        account.save()

        # 결과 출력을 위해 업데이트된 데이터 보관
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

    # 업데이트된 데이터를 출력
    print_results(data)
    

class Command(BaseCommand):
    help = 'Reset Limits'

    def add_arguments(self, parser):
        parser.add_argument('type', type=str)
        parser.add_argument('time', type=str)

    def check_argument(self, reset_type, argument):

        if reset_type == 'cron':
            if not re.match(r'^(([01]\d|2[0-3]):([0-5]\d))$', argument):
                raise argparse.ArgumentTypeError("'{0}' is not a valid HOUR(00-23):MINUTE(00-59) format"\
                                                .format(argument))
            
        elif reset_type == 'interval':
            if not re.match(r'^[0-9]+$', argument):
                raise argparse.ArgumentTypeError("'{0}' is not a valid INTEGER format"\
                                                .format(argument))

        return True
            
    def handle(self, *args, **options):


        # 리셋 타입 받아옴 cron / interval
        reset_type = options['type']

        reset_hour, reset_minute, reset_delay = 0, 0, 0
        total_wait_to_second = 0

        if reset_type == 'cron':

            reset_time = options['time']

            # 시간 포맷에 맞는지 유효성 검사
            self.check_argument(reset_type, reset_time)

            # 타입이 cron 이라면 리셋을 원하는 시간과 분을 파라미터로 부터 가져옴
            reset_hour, reset_minute = [int(i) for i in reset_time.split(':')]
            
            # 현재 시간을 계산
            now_time = datetime.datetime.now()

            wait_time = None

            # 리셋을 원하는 시간:분 을 datetime 객체로 생성하는데, 현재 시간에서 시간과 분만 대체
            reset_time = now_time.replace(
                hour=reset_hour, 
                minute=reset_minute
            )

            # 만약 리셋을 원하는 타임이 지금 시간보다 작다면 다음날 해당 시간으로 설정
            if reset_time < now_time:
                reset_time = reset_time.replace(day=(now_time.day+1)) 

            # 현재 시간과 리셋을 원하는 시간의 차이를 계산하여 기다려야하는 시간을 datetime 객체로 생성
            wait_time = reset_time - now_time

            # 기다려야하는 시간을 초로 계산
            total_wait_seconds = int(wait_time.total_seconds())

            if reset_time > now_time:
                total_wait_seconds -= now_time.second

        elif reset_type == 'interval':
            # 타입이 interval 이라면 리셋을 원하는 지연 시간을 파라미터로 부터 가져
            reset_delay = options['time']

            # integer 포맷에 맞는지 유효성 검사
            self.check_argument(reset_type, reset_delay)

            reset_delay = int(reset_delay)

            # 해당 타입은 분 형태로 입력되었기 때문에 초 형태로 계산
            total_wait_seconds = (reset_delay * 60)

        else:
            return

        set_interval(reset_limits, total_wait_seconds, reset_type)
