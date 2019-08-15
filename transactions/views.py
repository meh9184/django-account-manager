from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ValidationError

from .forms import DepositForm,WithdrawForm,TransferForm
from .models import Withdraw,Deposit,Transfer

from users.models  import CustomUser, Account

def deposit_view(request, account_no):

    form = DepositForm(request.POST or None, account_no=account_no)

    if form.is_valid():
        deposit = form.save(commit=False)

        deposit.account = Account.objects.get(account_no=deposit.account_no)

        deposit.user_name = deposit.account.user.full_name
        deposit.save()

        deposit.account.balance += deposit.amount
        deposit.account.save()
        
        messages.success(request, 'You Have Deposited .'.format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "DW/dw.htm", context)

def withdraw_view(request, account_no):
    form = WithdrawForm(request.POST or None, account_no=account_no)

    if form.is_valid():
        withdraw = form.save(commit=False)

        withdraw.account = Account.objects.get(account_no=withdraw.account_no)

        # 1회 한도 초과되는지 검토
        if withdraw.account.limit_once < withdraw.amount:
            raise ValidationError("Can only withdraw up to . at a time".format(withdraw.account.limit_once))
        # 1일 한도 초과되는지 검토
        elif (withdraw.account.limit_daily - withdraw.amount) < 0:
            raise ValidationError("Expire daily withdraw limit")
        else:
            # 1일 제한량에서 amount 만큼 감소한 후 출금 진행
            withdraw.account.limit_daily -= withdraw.amount
            
            withdraw.user_name = withdraw.account.user.full_name
            withdraw.save()
            
            withdraw.account.balance-=withdraw.amount
            withdraw.account.save()

            messages.success(request, 'You Have Withdrawn .'.format(withdraw.amount))
            return redirect("home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "DW/dw.htm", context)

def transfer_view(request, account_no=False):
    form = TransferForm(request.POST or None, account_no=account_no)

    if form.is_valid():
        transfer = form.save(commit=False)
        transfer.account = Account.objects.get(account_no=transfer.account_no_from)

        commission = 500

        # 받는 계좌의 잔고를 누산
        receiver_obj = Account.objects.get(account_no=transfer.account_no_to)
        receiver_obj.balance += transfer.amount

        # 보내는 계좌와 받는 계좌의 은행이 다른지 확인 (같다면 수수료 면제)
        if transfer.account.bank != Account.objects.get(account_no=transfer.account_no_to).bank:
        
            # 보내는 계좌의 하루 이체 건수 확인
            if transfer.account.daily_transfer_number <= 0:
                # 초과했다면 수수료 500원 부과
                transfer.amount += commission
            else:
                # 초과하지 않았다면 이체 건수 하나 감소
                transfer.account.daily_transfer_number -= 1

        # 보내는 계좌의 잔고를 차감
        transfer.user_name = CustomUser.objects.get(email=request.user).full_name
        transfer.account.balance -= transfer.amount
        transfer.account.save()

        # 추가 정보 저장
        transfer.receiver_id = receiver_obj.user.id
        transfer.receiver_name = receiver_obj.user.full_name

        receiver_obj.save()
        transfer.save()
        

        messages.success(request, 'You Have Sent Money .'.format(transfer.amount))
        return redirect("home")

    context = {
        "title": "Transfer",
        "form": form
    }
    return render(request, "DW/dw.htm", context)


def transcations_detail(request):
    user = request.user
    dep_obj  = Deposit.objects.filter(user=user)
    with_obj = Withdraw.objects.filter(user=user)
    Td_obj   = Transfer.objects.filter(user=user)
    Tc_obj   = Transfer.objects.filter(receiver_id=user.id)

    context={
        'dep_obj':dep_obj,
        'with_obj':with_obj,
        'Td_obj':Td_obj,
        'Tc_obj':Tc_obj,
    }

    return render(request,'Trans/trans.htm', context)


def transcations_summary(request):
    user = request.user
    dep_obj  = Deposit.objects.filter(user=user)
    with_obj = Withdraw.objects.filter(user=user)
    Td_obj   = Transfer.objects.filter(user=user)
    Tc_obj   = Transfer.objects.filter(receiver_id=user.id)

    context={
        'dep_obj':dep_obj,
        'with_obj':with_obj,
        'Td_obj':Td_obj,
        'Tc_obj':Tc_obj,
    }

    return render(request,'Trans/mini.htm', context)


def transcations_timeline(request):
    
    dep_obj  = Deposit.objects.filter(user_name=request.user.full_name)
    with_obj = Withdraw.objects.filter(user_name=request.user.full_name)
    Td_obj   = Transfer.objects.filter(user_name=request.user.full_name)
    Tc_obj   = Transfer.objects.filter(receiver_name=request.user.full_name)

    for obj in Td_obj:
        obj.set_action_name('Transfer_debit')
    for obj in Tc_obj:
        obj.set_action_name('Transfer_credit')


    # 모든 트랜젝션을 한 종류의 객체로 취급
    # 4 종류의 객체를 정리하여 리스트 만들고 timestamp 기준으로 정렬
    from itertools import chain
    from operator import attrgetter

    transactions_hub = list(chain(dep_obj, with_obj, Td_obj, Tc_obj))          
    transactions_hub = sorted(
        chain(dep_obj, with_obj, Td_obj, Tc_obj),
        key = attrgetter('timestamp'), 
        reverse=True
    )

    # 트랜젝션 날짜별 그룹핑 작업
    transactions_by_date = dict()

    # 모든 트랜젝션을 순회하면서
    for transaction in transactions_hub:

        # 트랜젝션의 날짜를 조회
        date = transaction.timestamp.strftime('%m월 %d일 ')
        day = transaction.timestamp.strftime('%A')

        # 요일 한글 명칭으로 변환
        day_for_kor = {
            'Monday': '월요일',
            'Tuesday': '화요일',
            'Wednesday': '수요일',
            'Thursday': '목요일',
            'Friday': '금요일',
            'Saturday': '토요일',
            'Sunday': '일요일',
        }

        date += day_for_kor[day]

        # 만약 해당 날짜가 Dict에 key로 이미 존재한다면 
        if date in transactions_by_date.keys():
            transactions_by_date[date].append(transaction)

        # 만약 존재하지 않는다면
        else:
            # key 값으로 리스트를 만들고 트랜젝션을 삽입
            transactions_by_date[date] = list()
            transactions_by_date[date].append(transaction)
        

    context={
        'count_dep': len(dep_obj),
        'count_with': len(with_obj),
        'count_Td': len(Td_obj),
        'count_Tc': len(Tc_obj),
        'transactions_by_date': transactions_by_date,
        'transactions': transactions_hub,
        'count': len(transactions_hub),
        'title': 'Timeline'
    }

    return render(request,'Trans/timeline.html', context)